import bpy
from bpy.types import PropertyGroup, Image, Panel
from bpy import ops as OP
from bpy.props import (
    StringProperty, CollectionProperty, BoolProperty,
    PointerProperty, IntProperty, IntVectorProperty, IntProperty
)
from . functions import get_corner_points_from_bb_relative_to_view, view3d_utils


SCENE_MAX_BUTTONS = 1024
LAYER_MAX_BUTTONS = 32


class PK_Layer(PropertyGroup):
    ''' The optimal should be a list of integers that mark each index,
        the bad thing is we can't predict the size of the array to use Blender Properties
        also, a string property to save the indices is size limited... :(
        and a typical python list will be cleaned when closing Blender...
        BUT! We can store it in a text file and just load it on start and save when adding buttons/editing layers...
        Our text file can be a pointer to a text file inside Blender as well as file_path for an external file.
    '''
    # We need a name to name the text file, if this is None we will look into database directory.
    name : StringProperty(default="Layer_", name="Layer Name")

    # Limited to 32 buttons per layer.
    current_button_index : IntProperty(default=0, min=-1, max=LAYER_MAX_BUTTONS-1)
    button_indices : IntVectorProperty(default=[-1]*LAYER_MAX_BUTTONS, size=LAYER_MAX_BUTTONS, min=-1, max=SCENE_MAX_BUTTONS)
    # indices : CollectionProperty(type=IntProperty)

    # button_indices = [] # cached like of button_indices_str
    # button_indices_text : PointerProperty(type=Text, name="Button Indices Text")

    '''
     Each layer could have it's name, icon, color...
    '''
    text : StringProperty(default="Layer", name="Layer")
    icon : PointerProperty(type=Image, name="Icon")
    icon_path : StringProperty(default="", subtype='FILE_PATH', name="Icon Path")

    # WE NEED SOME ATTR TO KNOW IF THE LAYER IS ACTIVE !
    is_active : BoolProperty(default=True, name="Is Active")

    def add_button(self, button):
        if isinstance(button, int):
            self.button_indices[self.current_button_index] = button
            #self.button_indices.append(button)
        else:
            self.button_indices[self.current_button_index] = self.get_index(button)
            #self.button_indices.append(self.get_index(button))
        self.current_button_index += 1

    def remove_button(self, button):
        # print(list(self.button_indices))
        if isinstance(button, int):
            b_indice = button
            #self.button_indices.remove(button)
        else:
            b_indice = self.get_index(button)
            #self.button_indices.remove(self.get_index(button))
        found_button = False
        for idx, indice in enumerate(self.button_indices):
            if b_indice == indice:
                self.button_indices[idx] = -1
                found_button = True
            elif found_button:
                self.button_indices[idx] -= 1

        self.current_button_index -= 1
        self.update_indices(idx)
        # print(list(self.button_indices))

    def update_indices(self, removed_button_indice):
        # 1ST. Take good indices:
        good_indices = [indice for indice in self.button_indices if indice != -1]
        # REST OF INDICES ARE NON-VALID.
        for i in range(len(good_indices), LAYER_MAX_BUTTONS): # NOTE: what if len is LAYER_MAX_BUTTONS?
            good_indices.append(-1)
        self.button_indices = good_indices
        
    def reset_indices(self):
        for idx in self.button_indices:
            idx = -1

    def check_button(self, button):
        if isinstance(button, int):
            return button not in self.button_indices
        else:
            return self.get_index(button) not in self.button_indices

    def get_index(self, button):
        return button.index

    def toggle(self):
        self.is_active = not self.is_active

    def show_context_menu(self, context):
        active_picker = context.scene.pickers.active_picker()
        if not active_picker:
            print("ERROR: Active Picker")
            return
        active_scene = active_picker.get_active_scene()
        if not active_scene:
            print("ERROR: Active Scene")
            return
        active_view = active_scene.get_active_view()
        if not active_view:
            print("ERROR: Active View")
            return
        ok = False
        for index, l in enumerate(active_view.layers):
            if l == self:
                ok = True
                print(index)
                active_view.active_layer = index
                break
        if ok:
            # context.scene.widgets.active = [self.w_index, self.b_index, -1]
            OP.wm.call_panel(name="PK_PT_layer_context_menu", keep_open=True)
        return

    def add_selected_pose_bones(self, context, scene):

        # Scene/View vars.
        buttons = scene.buttons
        num_bones = len(buttons)
        active_view = scene.active_view
        view = scene.get_active_view()
        pk = context.scene.pickers.active_picker()
        layer_index = 0

        for idx, layer in enumerate(view.layers):
            if self == layer:
                layer_index = idx
                break
        
        context.active_object.data.pose_position = 'REST'
        
        ''' PROJECTION SETUP '''
        # Change to object. (just for 'well-framing')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get 3d region.
        region = context.region
        area = context.area
        space_data = context.space_data
        region3d = context.area.spaces.active.region_3d

        # Back-Up matrix data.
        old_is_perspective      = region3d.is_perspective * True
        old_view_matrix         = region3d.view_matrix * 1 # just a trick to ensure it's not a reference # TODO: remove
        old_view_perspective    = region3d.view_perspective * 1
        old_view_location       = region3d.view_location * 1
        old_view_rotation       = region3d.view_rotation * 1
        old_view_camera_zoom    = region3d.view_camera_zoom * 1

        # View camera to specific view.
        bpy.ops.view3d.view_axis(type=view.view) # NOTE: take care...
        # Fit view to target.
        bpy.ops.view3d.view_selected(use_all_regions=False)
        # Update Matrix.
        region3d.update()

        # Return to Pose Mode.
        bpy.ops.object.mode_set(mode='POSE')

        # GET PROJECTED POINTS AND SIZE FROM ARMATURE OBJECT AND MESH BOUNDS
        # Get specific bound points per view.
        bounds = get_corner_points_from_bb_relative_to_view(context.active_object, view.view)
        # Get 2D Screen projected Positions.
        a = view3d_utils.location_3d_to_region_2d(region, space_data.region_3d, bounds[0], default=None)
        b = view3d_utils.location_3d_to_region_2d(region, space_data.region_3d, bounds[1], default=None)
        # Extend bounds of armature/skeleton to have some margins.
        A = (int(a[0]) - 10, int(a[1]) + 10)
        B = (int(b[0]) - 10, int(b[1]) + 10)
        # Get projected size.
        _w = abs(B[0] - A[0])
        _h = abs(B[1] - A[1])
        # Get projected origin points.
        xo = A[0] if A[0] < B[0] else B[0]
        yo = A[1] if A[1] < B[1] else B[1]

        # Get sizes of image (less margins * 2 (both sides))
        o = pk.pos
        theme = pk.theme
        scene_pos = (o[0] + theme.layerbar_width + 10, o[1] + 10)
        scene_size = (pk.size[0] - theme.layerbar_width - 20, pk.size[1] - theme.menubar_height - 35)
        #scene_pos = (pk.pos[0] + theme.layerbar_width + 10, pk.pos[1] + 10)
        #scene_size = (pk.size[0] - theme.layerbar_width - 20, pk.size[1] - theme.menubar_height - 35)
        image = view.image
        if image:
            s = view.image.size
            p = s[1] / s[0]
            if s[1] > s[0]:
                h = scene_size[1]
                w = h / p
                if w > scene_size[0]:
                    x = scene_pos[0]
                    w = scene_size[0]
                    h = w * p
                else:
                    off_x = scene_size[0] - w
                    x = scene_pos[0] + abs(off_x / 2.0)
                y = scene_pos[1]
                xo += 10 # add the spacing/margins (as it will rest it at the end)
                # xo = x
            else:
                w = scene_size[0]
                h = w * p
                if h > scene_size[1]:
                    y = scene_pos[1]
                    j = scene_size[1]
                    w = h / p
                else:
                    off_y = scene_size[1] - h
                    y = scene_pos[1] + abs(off_y / 2.0)
                x = scene_pos[0]
                yo += 10 # add the spacing/margins (as it will rest it at the end)
                # yo = y
            # xo = int(x)
            # yo = int(y)
        else:
            w, h = scene_size # size[0] - 20, size[1] - 20
        # Get relation between sub-spaces.
        relX = w / max(0.01, _w)
        relY = h / max(0.01, _h)

        # Armature Object Matrix World.
        mw = pk.arm_obj.matrix_world

        # Loop over selected bones in Pose Mode.
        new_button_list = []
        for bone in context.selected_pose_bones:
            button = buttons.get(bone.name, None)
            if not button:
                button = scene.buttons.add()
                new_button_list.append(button)
                # Button.
                bone_name = bone.name.upper()
                button.name = bone.name
                button.index = num_bones
                button.text = 'IK' if 'IK' in bone_name else 'FK' if 'FK' in bone_name else ''

                # Button Data.
                b_data = button.get_data_from_view_index(active_view)
                b_data.layer = layer_index
                b_data.layer_users = button.active_layer_users = 1
                b_data.is_active = b_data.is_visible = True

                # Project button from view.
                PK_Layer.project_bone_to_picker(
                    context,
                    mw,
                    bone,
                    b_data,
                    xo, yo,
                    relX, relY
                )

                # Calculate the factor [0-1].
                b_data.factor = [b_data.pos[0]/w, b_data.pos[1]/h]
                #b_data.pos[0] -= 7
                #b_data.pos[1] -= 7

                # Add button to view and layer.
                self.add_button(button)
                view.button_indices.append(button.index)

                num_bones += 1
            else:
                if not self.check_button(button):
                    # Button Data.
                    b_data = button.get_data_from_view_index(active_view)
                    b_data.layer = layer_index
                    b_data.layer_users += 1
                    b_data.active_layer_users += 1
                    b_data.is_active = b_data.is_visible = True

                    # Project button from view.
                    PK_Layer.project_bone_to_picker(
                        context,
                        mw,
                        bone,
                        b_data,
                        xo, yo,
                        relX, relY
                    )

                    # Calculate the factor [0-1].
                    b_data.factor = [b_data.pos[0]/w, b_data.pos[1]/h]
                    #b_data.pos[0] -= 7
                    #b_data.pos[1] -= 7

                    # Add button to view and layer.
                    self.add_button(button)
                    view.button_indices.append(button.index)
        
        # Ensure.
        '''
        from . ops_scene import get_scene_size, get_view_image_size
        active_scene = pk.get_active_scene()
        active_view_idx = active_scene.active_view
        active_view = active_scene.get_active_view()
        if active_view.image:
            w, h = get_view_image_size(pk, active_view)
        #else:
        #    w, h = get_scene_size(pk, True)
            for b in new_button_list:
                d = b.get_data_from_view_index(active_view_idx)
                d.pos = [int(w * d.factor[0]), int(h * d.factor[1])]
        '''
        
        # Recover values.
        region3d.is_perspective     = old_is_perspective
        region3d.view_matrix        = old_view_matrix
        region3d.view_perspective   = old_view_perspective
        region3d.view_location      = old_view_location
        region3d.view_rotation      = old_view_rotation
        region3d.view_camera_zoom   = old_view_camera_zoom
        
        context.active_object.data.pose_position = 'POSE'

    @staticmethod
    def project_bone_to_picker(context, armature_matrix_world, pose_bone, pk_button_data, xo, yo, relX, relY):
        # [NEW] Get Visual position of PoseBone and get center point.
        matrix_final = armature_matrix_world @ pose_bone.matrix
        vec = pose_bone.vector.normalized() * (pose_bone.bone.length / 2)
        matrix_final[0][3] += vec[0]
        matrix_final[1][3] += vec[1]
        matrix_final[2][3] += vec[2]

        # [NEW] Project bone center to screen space.
        center = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d, matrix_final.to_translation(), default=None)
        x, y = center

        # Transpose bone coords to fake origin.
        tranX = x - xo
        tranY = y - yo

        # Convert this coords to Picker UI space
        posX = tranX * relX
        posY = tranY * relY

        # Apply position, size and displace so for drawing offset etc...
        # pk_button_data.pos = [int(posX) - 7, int(posY) - 7] # Ensure is int.

        # UPDATE: USES POSITION AS CENTER
        pk_button_data.pos = [int(posX), int(posY)]
        # UPDATE: USES SIZE AS "RADIUS" (half the size)
        pk_button_data.size = [int(7), int(7)] # TODO: Should be possible to specify size.



class PK_Layer_ContextMenu(Panel):
    bl_idname = "PK_PT_layer_context_menu"
    bl_label = "Layer Properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "NONE"

    def draw(self, context):
        active_picker = context.scene.pickers.active_picker()
        if not active_picker:
            print("ERROR: Active Picker")
            return
        active_scene = active_picker.get_active_scene()
        if not active_scene:
            print("ERROR: Active Scene")
            return
        active_view = active_scene.get_active_view()
        if not active_view:
            print("ERROR: Active View")
            return
        layer = active_view.get_active_layer()
        if not layer:
            print("ERROR: Active Layer")
            return

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.separator()
        layout.label(text=layer.name, icon='RENDERLAYERS') # SEQ_STRIP_DUPLICATE

        main = layout.column(align=True)
        main.prop(layer, "text", text="Name")
        main.separator()
        main.prop(layer, "icon", text="Icon")
        main.prop(layer, "icon_path", text="Icon Path")
        main.separator()
        main.prop(layer, "is_active", text="Active")

        buttons = active_scene.buttons
        main.separator()
        box = main.box().column(align=True)
        for idx in layer.button_indices:
            if idx == -1:
                break
            row = box.row(align=True)
            row.label(text=buttons[idx].name)
            row.operator('pk.remove_button_from_layer', icon='REMOVE', text='').button_index = idx
