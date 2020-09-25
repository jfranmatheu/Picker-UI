import bpy
from bpy.types import Operator, WindowManager
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty


class PK_OT_clear_view(Operator):
    bl_idname = "pk.clear_view"
    bl_label = "Clear Active View :"
    bl_description = "Clear active view, removing all layers and buttons it has."
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1 and context.scene.pickers.data is not None

    def draw(self, context):
        self.layout.label(text="This will remove all your layers and buttons inside.")
        self.layout.alert = True
        self.layout.label(text="Are you sure?")

    def invoke(self, context, event):
        return WindowManager.invoke_props_dialog(self, width=300)

    def execute(self, context):
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
        active_scene.get_active_view().clear(active_scene)
        return {'FINISHED'}

class PK_OT_switch_view(Operator):
    bl_idname = "pk.switch_view"
    bl_label = "Switch View :"
    bl_description = "Switch active view to other view (2 views per scene)"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1 and context.scene.pickers.data is not None

    def execute(self, context):
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            self.report({'WARNING'}, "Picker has no scene")
            return {'CANCELLED'}
        active_scene = active_picker.scenes[active_picker.active_scene]
        if active_scene.active_view == -1:
            self.report({'WARNING'}, "Picker has no view")
            return {'CANCELLED'}
        active_scene.switch_view()
        return {'FINISHED'}
