import bpy
from bpy.types import Operator, WindowManager
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty


class PK_OT_remove_picker(Operator):
    bl_idname = "pk.remove_picker"
    bl_label = "Remove picker"
    bl_description = "Remove Picker UI (aka character)"
    bl_options = {'INTERNAL'}

    index : IntProperty(default=-1, name="Picker Index")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        if self.index == -1 or self.index >= len(context.scene.pickers.data):
            self.report({'WARNING'}, "Picker index out of bounds! (please report this)")
            return {'CANCELLED'}
        context.scene.pickers.remove(self.index)
        return {'FINISHED'}
