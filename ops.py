import bpy
from bpy.types import Operator
from . functions import (
    get_corner_points_from_bb_relative_to_view,
    convert_3d_spacecoords_to_2d_screencoords,
    viewport_screenshot
)
from bpy_extras import view3d_utils

# THIS OPERATOR WILL SETUP AND CREATE THE PICKER UI / WIDGET
class PK_OT_generate_picker(Operator):
    # We want to generate our picker graphics,
    #    create our picker data and fill data with buttons and so.
    bl_idname = "pk.generate_picker"
    bl_label = ""
    bl_description = "Generate Picker"

    @classmethod
    def poll(cls, context):
        # Armature slot should be something and we have to be in Pose mode.
        return context.mode == 'POSE' and context.window_manager.ui_data.armature_object

    def execute(self, context):
        create = context.window_manager.ui_data
        picker = None
        self.max_size = [100, 100]

        # TODO: we can give support for multi images for multiple views in the future...
        if not create.generate_picker_image:
            if create.views != 'FRONT':
                create.generate_picker_image = True
            elif create.generate_facial and create.facial_views != 'FRONT':
                create.generate_picker_image = True

        # GET POSE BONES
        if create.only_selected_pose_bones:
            self.pBones = [bone for bone in context.selected_pose_bones]
        else:
            self.pBones = create.armature_object.pose.bones

        # Get 3d region
        self.region = context.region
        self.area = context.area
        self.space_data = context.space_data
        region3d = context.area.spaces.active.region_3d

        # Back-Up matrix data
        old_is_perspective      = region3d.is_perspective * True
        old_view_matrix         = region3d.view_matrix * 1 # just a trick to ensure it's not a reference
        old_view_perspective    = region3d.view_perspective * 1
        old_view_location       = region3d.view_location * 1
        old_view_rotation       = region3d.view_rotation * 1
        old_view_camera_zoom    = region3d.view_camera_zoom * 1

        # MALLOC PICKER
        picker = context.scene.pickers.data.add()

        # SETUP SCENE/S
        self.create = create
        self.create_scene(context, region3d, create, picker, create.views, False)

        if create.generate_facial:
            self.create_scene(context, region3d, create, picker, create.facial_views, True)


        # FILL REST OF PICKER DATA
        picker.name = create.name
        picker.uuid = ""
        picker.arm_obj = create.armature_object
        picker.size = self.max_size

        # RETURN TO PREVIOUS VIEW AND MODE
        region3d.is_perspective     = old_is_perspective
        region3d.view_matrix        = old_view_matrix
        region3d.view_perspective   = old_view_perspective
        region3d.view_location      = old_view_location
        region3d.view_rotation      = old_view_rotation
        region3d.view_camera_zoom   = old_view_camera_zoom

        #return {'FINISHED'}
        # At the end - if all it's OK - we want to draw our picker.
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pk.draw_picker()
        return {'FINISHED'}

    def create_scene(self, context, region3d, create, picker, views, is_facial=False):
        #print("CreateScene::CONTEXT: ", context)
        # Create our scene
        pk_scene = picker.scenes.add()
        # Create Buttons
        self.create_buttons(pk_scene)

        if create.generate_default_layers:
            # Generate Layers
            self.generate_default_layers(pk_scene.layers, pk_scene.buttons)

        index = 0
        for view in views.split('_'):
            if view != "":
                # View camera to specific view
                bpy.ops.view3d.view_axis(type=view)
                # Fit view to target
                bpy.ops.view3d.view_selected(use_all_regions=False)
                # Update Matrix
                region3d.update()
                # Create and Setup View
                pk_view = pk_scene.views.add()
                pk_view.view = view.lower().capitalize()
                pk_view.name = picker.name.replace(' ', '') + "_View_" + str(index) + "_" + pk_view.view
                # Setup for side view for filtering
                pk_view.is_side_view = view in {'LEFT', 'RIGHT'}
                pk_view.exclude_buttons_filter = view[0].lower() if pk_view.is_side_view else ''
                # Create and setup View Filter
                self.setup_view_layer_indices(pk_view, pk_scene.layers)
                # Project buttons from view
                self.project_from_view(context, create, view, pk_view, pk_scene.buttons, is_facial)
                index += 1

    def to_screen_coords(self, point):
        return view3d_utils.location_3d_to_region_2d(self.region, self.space_data.region_3d, point, default=None)

    def generate_default_layers(self, pk_layers, buttons):
        from . pk_data import default_layers, MIRROR_LAYER, LEFT, RIGHT
        for layer in default_layers:
            if layer[1] == MIRROR_LAYER:
                self.setup_layer_buttons_indices(pk_layers, layer, buttons, LEFT)
                self.setup_layer_buttons_indices(pk_layers, layer, buttons, RIGHT)
            else:
                self.setup_layer_buttons_indices(pk_layers, layer, buttons, '')

    def setup_layer_buttons_indices(self, pk_layers, layer, buttons, sufix=''):
        pk_layer = pk_layers.add()
        pk_layer.text = layer[0] + sufix
        keys = layer[2]
        index = 0
        sufix = sufix.lower()
        using_sufix = sufix != ''
        color = getattr(self.create, layer[3] + sufix)
        for pk_button in buttons:
            bone_name = pk_button.name.lower()
            # USINF SUFIX, SO IT'S A SIDED LAYER
            if using_sufix:
                if sufix.lower() in bone_name:
                    if any(key in bone_name for key in keys):
                        self.fill_button(pk_layer, pk_button, index, color)
            elif any(key in bone_name for key in keys):
                self.fill_button(pk_layer, pk_button, index, color)
            index += 1

    def fill_button(self, layer, button, index, color):
        layer.button_indices.append(index)
        button.layer_users += 1
        button.active_layer_users += 1
        button.visible = True
        button.color = color

    def create_buttons(self, pk_scene):
        for bone in self.pBones:
            pk_button = pk_scene.buttons.add()
            pk_button.size = [int(20), int(20)]
            pk_button.text = bone.name
            pk_button.name = bone.name

    def setup_view_layer_indices(self, pk_view, pk_layers):
        if not pk_view.is_side_view:
            return
        # FILL LIST WITH INDICES BASED ON FILTER
        filter = pk_view.exclude_buttons_filter
        index = 0
        for layer in pk_layers:
            if filter not in layer:
                #layer_indices_str += ',' + str(index) # perma/scene
                pk_view.layer_indices.append(index) # temp/cached
            index += 1
        # FILL TEXT FILE WITH INDICES LIST
        pk_view.layer_indices_text = bpy.data.texts.new(pk_view.name)
        pk_view.layer_indices_text.from_string(str(pk_view.layer_indices)[1:-1])

    def project_from_view(self, context, create, view, pk_view, pk_buttons, is_facial=False):
        #print("ProjectFromview::CONTEXT: ", context)
        # GET PROJECTED POINTS AND SIZE FROM ARMATURE OBJECT AND MESH BOUNDS
        # Get specific bound points per view.
        bounds = get_corner_points_from_bb_relative_to_view(context.active_object, view)
        # Get 2D Screen projected Positions.
        a = self.to_screen_coords(bounds[0])
        b = self.to_screen_coords(bounds[1])
        # Extend bounds of armature/skeleton to have some margins.
        A = (int(a[0]) - 10, int(a[1]) + 10)
        B = (int(b[0]) - 10, int(b[1]) + 10)
        # Get projected size.
        self._w = abs(B[0] - A[0])
        self._h = abs(B[1] - A[1])
        # Get projected origin points.
        self.xo = A[0] if A[0] < B[0] else B[0]
        self.yo = A[1] if A[1] < B[1] else B[1]

        # GENERATE IMAGE AND GET SIZE AND SIZE RELATION
        # TO TRANSPOSE PROJECTED COORDS TO PICKER UI SPACE.
        # Generate Graphic for View
        if create.generate_picker_image:
            print("Generating Image...")
            image = self.generate_view_image(context, pk_view, is_facial)
        else:
            if is_facial:
                image = create.picker_facial_image
            else:
                image = create.picker_image
        pk_view.image = image
        img_size = image.size
        self.max_size = img_size if img_size[0] > self.max_size[0] or img_size[1] > self.max_size[1] else self.max_size
        # Get sizes of image (less margins * 2 (both sides))
        self.w, self.h = img_size[0] - 20, img_size[1] - 20
        # Get relation between sub-spaces.
        self.relX = self.w / self._w
        self.relY = self.h / self._h

        # GET EDIT BONES
        #bpy.ops.object.mode_set(mode='EDIT')
        #bones = create.armature_object.data.edit_bones

        index = 0
        for pbone in self.pBones:
            # TODO: calculate visual position of pose bones instead of taking edit bones position.
            self.project_bone_to_picker(context, pbone, pk_view, pk_buttons[index])
            index += 1


    def generate_view_image(self, context, pk_view, is_facial=False):
        #print("GenerateViewImage::CONTEXT: ", context)
        space   = self.space_data
        overlay = space.overlay
        shading = space.shading
        # BACK-UP SHADING PROPS
        show_overlays           = overlay.show_overlays * True
        show_gizmo              = space.show_gizmo * True
        background_type         = shading.background_type + ''
        background_color        = shading.background_color * 1
        color_type              = shading.color_type + ''
        light                   = shading.light + ''
        object_outline_color    = shading.object_outline_color * 1
        shading_type            = shading.type + ''
        show_object_outline     = shading.show_object_outline * True
        show_cavity             = shading.show_cavity * True
        show_shadows            = shading.show_shadows * True

        # CHANGE VIEWPORT SETTINGS TO RENDER
        overlay.show_overlays = False
        space.show_gizmo = False
        shading.background_type         = 'VIEWPORT'
        shading.background_color        = (0, 0, 0) # Black
        shading.color_type              = 'SINGLE'
        shading.single_color            = (.5,.5,.5)
        shading.light                   = 'FLAT'
        shading.show_object_outline     = True
        shading.object_outline_color    = (.2,.2,.2)
        shading.type                    = 'SOLID'
        shading.show_cavity             = True
        shading.show_shadows            = True

        # Redraw Window to update draw data
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) # TODO: better to refresh each area?

        # Create Picker Image
        name = "Picker_"
        name += "Facial_" + pk_view.view if is_facial else pk_view.view

        pk_image = viewport_screenshot(self.area.x + self.xo, self.area.y + self.yo, self._w, self._h, name)

        # Recover Viewport settings
        overlay.show_overlays           = show_overlays
        space.show_gizmo                = show_gizmo
        shading.background_type         = background_type
        shading.background_color        = background_color
        shading.color_type              = color_type
        shading.light                   = light
        shading.show_object_outline     = show_object_outline
        shading.object_outline_color    = object_outline_color
        shading.type                    = shading_type
        shading.show_cavity             = show_cavity
        shading.show_shadows            = show_shadows

        return pk_image


    def project_bone_to_picker(self, context, pose_bone, pk_view, pk_button):
        #print("ProjectBone::CONTEXT: ", context)
        # CHECK FOR ERRORS
        if pk_button.name != pose_bone.name:
            print("WARN: Button's name it's different from bone's name!")

        # [OLD (EditBone)] Project bone center to screen space.
        #center = convert_3d_spacecoords_to_2d_screencoords(context, bone.center)
        #x, y = center

        # [NEW] Get Visual position of PoseBone and get center point
        matrix_final = self.create.armature_object.matrix_world @ pose_bone.matrix
        vec = pose_bone.vector.normalized() * (pose_bone.bone.length / 2)
        matrix_final[0][3] += vec[0]
        matrix_final[1][3] += vec[1]
        matrix_final[2][3] += vec[2]

        # [NEW] Project bone center to screen space.
        center = self.to_screen_coords(matrix_final.to_translation())
        x, y = center

        # Transpose bone coords to fake origin.
        tranX = x - self.xo
        tranY = y - self.yo

        # Convert this coords to Picker UI space
        posX = tranX * self.relX
        posY = tranY * self.relY

        # Apply position
        if pk_view.is_side_view:
            pk_button.pos_side = [int(posX), int(posY)] # ensure is int
        else:
            pk_button.pos_front = [int(posX), int(posY)] # ensure is int

