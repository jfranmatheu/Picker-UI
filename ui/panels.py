from bpy.types import Panel, UILayout


class PickerUIPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Rig'

    bl_idname = "PK_PT_picker_ui"
    bl_label = "Picker UI"

    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'

    def draw(self, context):
        pass


class SetupPickerUI(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Rig'

    bl_parent_id = 'PK_PT_picker_ui'
    bl_label = 'Setup Picker'
    bl_idname = "PK_PT_setup_picker_ui"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw(self, context):
        pk = context.window_manager.ui_data
        
        layout = self.layout
        col = layout.column(align=True)

        col.prop(pk, 'armature')

        if not pk.armature:
            return

        col.prop(pk, 'picker_name')
        col.prop(pk, 'generate_picker_image')
        # row = col.row()
        # row.enabled = not pk.generate_picker_image
        if pk.generate_picker_image:
            col.prop(pk, 'view')
        else:
            col.prop(pk, 'picker_image')
        
        col.prop(pk, 'add_selected_bones', text="Add selected bones")

        op = layout.row()
        op.scale_y = 1.25
        op.operator('pk.create_picker', text="Create Picker")

        if len(context.scene.pickers.data) > 0:
            op = layout.row()
            op.scale_y = 1.25
            op.operator('pk.draw_picker', text="Draw Picker")


class ListPickerUI(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Rig'

    bl_parent_id = 'PK_PT_picker_ui'
    bl_label = 'My Pickers'
    bl_idname = "PK_PT_list_picker_ui"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    def draw(self, context):
        pks = context.scene.pickers

        layout = self.layout
        
        if not pks.data:
            layout.alert = True
            layout.label(text="No PickerUI created")
            return
        
        col = layout.column(align=True)
        
        for i, pk in enumerate(pks.data):
            row = col.row(align=True)
            row.operator('pk.draw_picker', text='', icon='PLAY').idx = i
            row.prop(pk, 'name', text='')
            row.alert = True
            row.operator('pk.remove_picker', text='', icon='TRASH').index = i
            
        
classes = (
    PickerUIPanel,
    SetupPickerUI,
    ListPickerUI
)

def register(reg):
    for cls in classes:
        reg(cls)

def unregister(unreg):
    for cls in reversed(classes):
        unreg(cls)