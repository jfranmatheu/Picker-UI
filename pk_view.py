from bpy.types import PropertyGroup, Image, Panel
from bpy import ops as OP
from bpy.props import (
    StringProperty, CollectionProperty, BoolProperty, EnumProperty,
    PointerProperty, FloatProperty, IntVectorProperty, IntProperty
)
from .pk_layer import PK_Layer


layer_items = [('NONE', "NONE", "")]

class PK_View(PropertyGroup):
    ''' Capas en forma de lista:
    def get_view_layer_as_enum(self, context):
        layer_items.clear()
        for layer in self.layers:
            layer_items.append((layer.name, layer.text, ""))
        if layer_items:
            return layer_items
        return [('NONE', "NONE", "")]
    layers_enum : EnumProperty(items=get_view_layer_as_enum, name="Layer List")
    '''
    
    view : StringProperty(default="FRONT", name="View")
    active_layer : IntProperty(default=-1, name="Active Layer")
    layers : CollectionProperty(type=PK_Layer, name="Layers")
    
    # al iniciar un picker ya creado,
    # esta lista se creará a partir de
    # los índices de botones de las layers (que no son una py list sino una lista de int vector ppt de Blender)
    button_indices = [] # cache for active buttons in view (indices)
    #buttons : CollectionProperty(type=PK_Button_Data, name="Buttons Data")
    buttons_offset : IntVectorProperty(default=[0, 0], size=2, name="Buttons Offset")

    ''' Maybe some mirror toggle for left/right? '''
    mirror : BoolProperty(default=False, name="Mirror View")
    is_side_view : BoolProperty(default=False, name="Is Side View")

    ''' Each view could have like it's own master layer,
        or maybe, layers are for each view and not for each entire picker.
        So, layers are generals for all views but each view has each own filters.
        Could be indices of each layer or buttons excluded?
        OK. Layer indices of layers to include in this view.
        PLUS, filter condition for buttons.
    '''
    name : StringProperty(default="View_", name="View Name")

    # NOTE: We don't need this anymore as we now store layers per view.
    #layer_indices = [] # cached like of layer_indices_str
    #layer_indices_text : PointerProperty(type=Text, name="Layer Indices Text")
    #exclude_buttons_filter = '' # to exclude buttons of other side when is_side_view (also will check for mirror)

    ''' Each view has each own image, preview of that view.
        If image is not in the project (picker is imported) we may need a path to it to reimport.
    '''
    image : PointerProperty(type=Image, name="Image")
    # We can just use the uuid from pk to know the path so:
    # data_dir>pk.uuid>"View_"+str(view_index)>image.png
    #image_path : StringProperty(default="", subtype='FILE_PATH', name="Image Path")
    image_opacity : FloatProperty(default=0.6, min=0, max=1, name="Image Opacity")

    def active_layers(self):
        return [layer for layer in self.layers if layer.is_active]

    def add_button(self, button):
        self.button_indices.append(self.get_index(button))

    def remove_button(self, button):
        if not isinstance(button, int):
            button = self.get_index(button)
        if button in self.button_indices:
            self.button_indices.remove(button)
        else:
            print("PK_VIEW::remove_button - Button index not found", button)

    def check_button(self, button):
        return self.get_index(button) in self.button_indices
    
    def has_button_index(self, index):
        return index in self.button_indices

    def get_index(self, button):
        return button if isinstance(button, int) else button.index

    def get_active_layer(self):
        return self.layers[self.active_layer] if self.active_layer != -1 else None

    def update_indices(self, buttons_to_update):
        for idx, b_indice in enumerate(self.button_indices):
            if b_indice in buttons_to_update:
                self.button_indices[idx] -= 1
        #for idx in buttons_to_update:
        #    # NOTE: Check this for future.
        #    self.button_indices[idx] = idx - 1
    
    def remove_layer(self, index):
        self.layers.remove(index)
        
    def clear(self, scene, use_cached_indices = False):
        # 1st method... #
        scene.print_button()
        
        # Remove buttons.
        buttons = scene.buttons

        if use_cached_indices:
            # FASTER METHOD BUT UNSAFE.
            self.button_indices.sort(reverse=True)
            for idx in self.button_indices:
                buttons[idx].remove(scene, True)
        else:
            # METHOD MORE SAFE BUT EXPENSIVE.
            for idx, button in enumerate(reversed(buttons)):
                buttons[idx].remove(scene, True)

        # Remove Layers.
        n = len(self.layers) - 1
        for idx, layer in enumerate(reversed(self.layers)):
            layer.reset_indices()
            self.layers.remove(n - idx)
        self.active_layer = -1

        # Reset View.
        self.button_indices.clear()
        
        scene.print_button()
        
        # 2nd method... #
        ''' 
        # Get other view just to compare.
        other = scene.get_other_view()
        # Remove buttons.
        buttons = scene.buttons
        buttons_to_remove = []
        if use_cached_indices:
            # FASTER METHOD BUT UNSAFE.
            for idx in self.button_indices:
                if not other.has_button_index(idx):
                    print("Button %s with index %i will be removed from Scene." % (buttons[idx].name, idx))
                    buttons_to_remove.append(idx)
                else:
                    print("Button %s with index %i will be removed from Active View." % (buttons[idx].name, idx))
                    buttons[idx].get_data_from_view_index(view_idx).is_active = False
        else:
            # METHOD MORE SAFE BUT EXPENSIVE.
            view_idx = scene.active_view
            other_view_idx = 0 if view_idx == 1 else 1
            for idx, button in enumerate(buttons):
                if button.get_data_from_view_index(view_idx).is_active:
                    if not button.get_data_from_view_index(other_view_idx).is_active:
                        print("Button %s with index %i will be removed from Scene." % (buttons[idx].name, idx))
                        buttons_to_remove.append(idx)
                    else:
                        print("Button %s with index %i will be removed from Active View." % (buttons[idx].name, idx))
                        button.get_data_from_view_index(view_idx).is_active = False
                    
        self.button_indices.clear()
        
        # Ensure order and make it reversed, this way indices won't scroll.
        buttons_to_remove.sort(reverse=True)
        
        scene.print_button()
        
        for button in buttons_to_remove:
            buttons.remove(idx)

        scene.update_indices(idx)
        scene.print_button()
        '''
            

    def load_image(self):
        if self.image:
            self.image.gl_load()

    def free_image(self):
        if self.image:
            self.image.gl_free()

    def generate_image(self, context, view):
        if self.image:
            self.image.gl_free()
            self.image.buffers_free()

        # Get 3d region
        region = context.region
        area = context.area
        space_data = context.space_data
        region3d = context.area.spaces.active.region_3d

        # Back-Up matrix data
        old_is_perspective      = region3d.is_perspective * True
        old_view_matrix         = region3d.view_matrix * 1 # just a trick to ensure it's not a reference
        old_view_perspective    = region3d.view_perspective * 1
        old_view_location       = region3d.view_location * 1
        old_view_rotation       = region3d.view_rotation * 1
        old_view_camera_zoom    = region3d.view_camera_zoom * 1

        # View camera to specific view
        bpy.ops.view3d.view_axis(type=view)
        # Fit view to target
        bpy.ops.view3d.view_selected(use_all_regions=False)
        # Update Matrix
        # region3d.update()


        # RETURN TO PREVIOUS VIEW AND MODE
        region3d.is_perspective     = old_is_perspective
        region3d.view_matrix        = old_view_matrix
        region3d.view_perspective   = old_view_perspective
        region3d.view_location      = old_view_location
        region3d.view_rotation      = old_view_rotation
        region3d.view_camera_zoom   = old_view_camera_zoom

    def show_layer_selector(self):
        if self.layers_enum != 'NONE' and self.layers:
            OP.wm.call_panel(name="PK_PT_view_layer_selector", keep_open=False)
            return True
        return False

'''
class PK_View_Layer_Selector(Panel):
    bl_idname = "PK_PT_view_layer_selector"
    bl_label = "Layer Selector"
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
        self.layout.label(text="Select a layer :")
        self.layout.prop(active_view, 'layers_enum', text='')
        self.layout.operator('pk.layer_add_selected_buttons', text="Add buttons to layer")
'''
