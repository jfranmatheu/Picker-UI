import bpy
from bpy.types import Operator, WindowManager
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty

from .pk_character import PK_Character


def get_scene_size(pk, with_margins=False):
    if with_margins:
        # In EDIT MODE take into account the tool bar space.
        if pk.mode == 1:
            return [pk.size[0] - pk.theme.layerbar_width - 20 - pk.theme.toolbar_width, pk.size[1] - pk.theme.menubar_height - pk.theme.statusbar_height - 35]
        else:
            return [pk.size[0] - pk.theme.layerbar_width - 20, pk.size[1] - pk.theme.menubar_height - pk.theme.statusbar_height - 35]
    else:
        return (pk.size[0] - pk.theme.layerbar_width, pk.size[1] - pk.theme.menubar_height - pk.theme.statusbar_height)

def get_view_image_size(pk, view):
    scene_size = get_scene_size(pk, True)
    if not view.image:
        return scene_size[0], scene_size[1]
    s = view.image.size
    p = s[1] / s[0]
    if s[1] > s[0]:
        h = scene_size[1]
        w = h / p
        if w > scene_size[0]:
            w = scene_size[0]
    else:
        w = scene_size[0]
        if h > scene_size[1]:
            w = h / p
    return w, h
    
''' NEW PICKER SCENE
    active_picker > scene
'''
class PK_OT_create_scene(Operator):
    bl_idname = "pk.create_scene"
    bl_label = "Create Picker Scene :"
    bl_description = "Create new scene in active picker"
    bl_options = {'INTERNAL'}

    scene_name : StringProperty(default='', name="Scene Name")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1 and context.scene.pickers.data is not None

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, 'scene_name')

    def invoke(self, context, event):
        return WindowManager.invoke_props_dialog(self, width=250)

    def execute(self, context):
        if self.scene_name == '' or self.scene_name.isspace():
            self.report({'WARNING'}, "scene name field is empty or invalid")
            return {'CANCELLED'}
        create = context.window_manager.ui_data
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        num = len(active_picker.scenes)
        new_scene = active_picker.scenes.add()
        if not new_scene:
            self.report({'WARNING'}, "Can't create new scene! (please report this)")
            return {'CANCELLED'}
        new_scene.name = self.scene_name
        new_scene.active_view = 0
        active_picker.active_scene = num
        return {'FINISHED'}


''' REMOVE PICKER SCENE
    active_picker > scene
'''
class PK_OT_remove_scene(Operator):
    bl_idname = "pk.remove_scene"
    bl_label = "Remove Active Scene :"
    bl_description = "Remove acive scene in active picker"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1 and context.scene.pickers.data is not None

    def execute(self, context):
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            self.report({'WARNING'}, "Picker has no scenes!")
            return {'CANCELLED'}
        if active_picker.active_scene <= len(active_picker.scenes) - 1:
            active_picker.scenes.remove(active_picker.active_scene)
            active_picker.active_scene = len(active_picker.scenes) - 1
        else:
            self.report({'WARNING'}, "Active Scene index ouside bounds! (please report this)")
            return {'CANCELLED'}
        return {'FINISHED'}

''' CHANGE PICKER SCENE
    active_picker > scene
'''

'''
scene_list_items = [('NONE', "None", "There are no scenes available")]
_scenes = []
def get_scene_list(self, context):
    pickers = context.scene.pickers
    active_picker = pickers.data[pickers.active_index]
    if not active_picker:
        return [('NONE', "None", "There are no scenes available")]
    scene_list_items.clear()
    _scenes.clear()
    active_scene = active_picker.active_scene
    active = None
    for i, scene in enumerate(active_picker.scenes):
        if i == active_scene:
            name = scene.name if scene.name != '' else 'Scene_'+str(i)
            scene_list_items.append((name, name, ""))
        else:
            name = scene.name if scene.name != '' else 'Scene_'+str(i)
            _scenes.append(name)
    for _name in _scenes:
        scene_list_items.append((_name, _name, ""))
    if not scene_list_items:
        return [('NONE', "None", "There are no scenes available")]
    return scene_list_items
'''

class PK_OT_change_scene_selector(Operator):
    bl_idname = "pk.change_scene_selector"
    bl_label = "Change Picker Scene :"
    bl_description = "Change active scene in active picker"
    bl_options = {'INTERNAL'} #, 'REGISTER', 'UNDO'}

    #scene_list : EnumProperty(name="Scene List", items=get_scene_list)

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1 and context.scene.pickers.data is not None

    '''
    def draw(self, context):
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if not active_picker:
            return
        active_scene = active_picker.active_scene
        if active_scene == -1:
            return

        layout = self.layout
        layout.use_property_split = True

        layout.label(text="Active Scene: " + active_picker.get_active_scene().name)

        col = layout.column(align=True)
        col.scale_y = 1.1
        col.prop(self, 'scene_list', expand=True)

        #for idx, scene in enumerate(active_picker.scenes):
        #    row = layout.row()
        #    row.active_default = active_scene == idx
        #    row.operator('pk.change_scene', text=scene.name).scene_index = idx
    '''

    def invoke(self, context, event):
        def draw(self, context):
            pickers = context.scene.pickers
            active_picker = pickers.data[pickers.active_index]
            if not active_picker:
                return
            active_scene = active_picker.active_scene
            if active_scene == -1:
                return
            layout = self.layout
            layout.scale_y = 1.1
            for idx, scene in enumerate(active_picker.scenes):
                row = layout.row()
                row.active_default = active_scene == idx
                row.operator('pk.change_scene', text=scene.name if scene.name != '' else 'Scene_' + str(idx)).scene_index = idx
        context.window_manager.popup_menu(draw, title="Scenes", icon='SCENE_DATA')
        return WindowManager.invoke_confirm(self, event)
        return {'FINISHED'}
        #return WindowManager.invoke_props_popup(self, event) # necesita register undo
        #return WindowManager.invoke_popup(self, width=250)

    '''
    def execute(self, context):
        if self.scene_list == 'NONE':
            self.report({'WARNING'}, "Can't switch scene. Scene not valid! (please report this)")
            return {'CANCELLED'}
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if not active_picker:
            self.report({'WARNING'}, "Can't switch scene. Picker not valid (please report)")
            return {'CANCELLED'}
        view = active_picker.get_active_view()
        if view:
            view.free_image()
        for idx, scene in enumerate(active_picker.scenes):
            if scene.name == self.scene_list:
                active_picker.active_scene = idx
                view = scene.get_active_view()
                if view:
                    view.load_image()
                break
        return {'FINISHED'}
    '''


class PK_OT_change_scene(Operator):
    bl_idname = "pk.change_scene"
    bl_label = "Change Picker Scene :"
    bl_description = "Change active scene in active picker"
    bl_options = {'INTERNAL'}

    scene_index : IntProperty(name="Scene Index", default=-1)

    def execute(self, context):
        if self.scene_index == -1:
            self.report({'WARNING'}, "Can't switch scene. Index not valid! (please report this)")
            return {'CANCELLED'}
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if not active_picker:
            self.report({'WARNING'}, "Can't switch scene. Picker not valid (please report)")
            return {'CANCELLED'}
        view = active_picker.get_active_view()
        if view:
            view.free_image()
        active_picker.active_scene = self.scene_index
        view = active_picker.get_active_view()
        if view:
            view.load_image()
        return {'FINISHED'}
