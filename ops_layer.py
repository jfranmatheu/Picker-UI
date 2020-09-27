import bpy
from bpy.types import Operator, WindowManager
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty


''' CREATE A PICKER LAYER
    active_picker > active_scene > active_view > layers
'''
class PK_OT_create_layer(Operator):
    bl_idname = "pk.create_layer"
    bl_label = "Create Picker Layer :"
    bl_description = "Create new layer in active picker"
    bl_options = {'INTERNAL'}

    layer_name : StringProperty(default='', name="Layer Name")
    add_selected_bones : BoolProperty(default=False, name="Add selected bones to layer")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, 'layer_name')
        checkbox = layout.column()
        if context.mode != 'POSE':
            checkbox.enabled = False
            checkbox.alert = True
            checkbox.label(text="* Only in pose mode *")
        checkbox.prop(self, 'add_selected_bones')

    def invoke(self, context, event):
        #pickers = context.scene.pickers.lock_ui = True
        return WindowManager.invoke_props_dialog(self, width=250)
        #pickers = context.scene.pickers.lock_ui = False
        #if signal:
        #    return signal
        #return {'FINISHED'}

    def execute(self, context):
        if self.layer_name == '' or self.layer_name.isspace():
            self.report({'WARNING'}, "layer name field is empty or invalid")
            return {'CANCELLED'}
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            self.report({'WARNING'}, "Picker has no scene")
            return {'CANCELLED'}
        active_scene = active_picker.scenes[active_picker.active_scene]
        if active_scene.active_view == -1:
            self.report({'WARNING'}, "Picker has no view")
            return {'CANCELLED'}
        # active_view = active_scene.views[active_scene.active_view]
        active_view = active_scene.get_active_view()
        # Create LAYER and fill data
        pk_layer = active_view.layers.add()
        pk_layer.name = "Layer_" + self.layer_name
        pk_layer.text = self.layer_name
        # pk_layer.button_indices = []
        # pk_layer.button_indices_text = bpy.data.texts.new(pk_layer.name)
        pk_layer.is_active = True

        if self.add_selected_bones:
            if context.mode == 'POSE' and context.selected_pose_bones:
                pk_layer.add_selected_pose_bones(context, active_scene)
            else:
                self.report({'WARNING'}, "Can't add bones. Not in pose mode or not bones selected")
        return {'FINISHED'}

class PK_OT_remove_button_from_layer(Operator):
    bl_idname = "pk.remove_button_from_layer"
    bl_label = "Remove Button from Active Layer :"
    bl_options = {'INTERNAL'}

    button_index : IntProperty(default=-1, name="Button Index")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        if self.button_index == -1:
            self.report({'WARNING'}, "Button index is invalid! (please report this)")
            return {'CANCELLED'}
        active_scene = context.scene.pickers.active_scene()
        if not active_scene:
            self.report({'WARNING'}, "Picker has no scene")
            return {'CANCELLED'}
        if active_scene.active_view == -1:
            self.report({'WARNING'}, "Picker has no view")
            return {'CANCELLED'}

        active_view = active_scene.get_active_view()
        layer = active_view.get_active_layer()
        button = active_scene.buttons[self.button_index]

        #layer.remove_button(self.button_index)
        if button.get_data_from_view_index(active_scene.active_view).layer != active_view.active_layer:
            self.report({'WARNING'}, "Button layer and active layer are different ones! (please report this)")
            print(button.get_data_from_view_index(active_scene.active_view).layer)
            print(active_view.active_layer)
            return {'CANCELLED'}
        button.remove(active_scene, True)
        context.area.tag_redraw()
        return {'FINISHED'}

layer_items = [('NONE', "NONE", "")]
def get_view_layer_as_enum(self, context):
    active_picker = context.scene.pickers.active_picker()
    if not active_picker:
        print("ERROR: Active Picker")
        return [('NONE', "NONE", "")]
    active_scene = active_picker.get_active_scene()
    if not active_scene:
        print("ERROR: Active Scene")
        return [('NONE', "NONE", "")]
    active_view = active_scene.get_active_view()
    if not active_view:
        print("ERROR: Active View")
        return [('NONE', "NONE", "")]
    layer_items.clear()
    for layer in active_view.layers:
        layer_items.append((layer.name, layer.text, ""))
    if layer_items:
        return layer_items
    return [('NONE', "NONE", "")]

class PK_OT_layer_add_selected_buttons(Operator):
    bl_idname = "pk.layer_add_selected_buttons"
    bl_label = "Select a layer :"
    bl_description = "Add selected buttons to selected layer"
    bl_options = {'INTERNAL'}

    layers_enum : EnumProperty(items=get_view_layer_as_enum, name="Layer List")
    #only_active_bone : BoolProperty(default=False, name="Add only active bone")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def draw(self, context):
        self.layout.prop(self, 'layers_enum', text='')
        #self.layout.operator('pk.layer_add_selected_buttons', text="Add buttons to layer")
        #self.layou.prop(self, 'only_active_bone')

    def invoke(self, context, event):
        return WindowManager.invoke_props_dialog(self, width=250)

    def execute(self, context):
        if self.layers_enum in {'', 'NONE'} or self.layers_enum.isspace():
            self.report({'WARNING'}, "Selected layer is invalid or picker has no layers")
            return {'CANCELLED'}
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            self.report({'WARNING'}, "Picker has no scene")
            return {'CANCELLED'}
        active_scene = active_picker.scenes[active_picker.active_scene]
        if active_scene.active_view == -1:
            self.report({'WARNING'}, "Picker has no view")
            return {'CANCELLED'}
        # active_view = active_scene.views[active_scene.active_view]
        active_view = active_scene.get_active_view()
        pk_layer = active_view.layers.get(self.layers_enum, None)
        if not pk_layer:
            self.report({'WARNING'}, "Selected layer not found! (please report this)")
            return {'CANCELLED'}
        if context.mode == 'POSE' and context.selected_pose_bones:
            pk_layer.add_selected_pose_bones(context, active_scene)
        else:
            self.report({'WARNING'}, "Can't add bones. Not in pose mode or not bones selected")
        return {'FINISHED'}
    