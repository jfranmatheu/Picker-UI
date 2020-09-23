from bpy.types import Panel


class PK_PT_setup_picker_panel(Panel):
    bl_label = "Setup Picker"
    bl_category = 'Rig'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 0
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pk = context.window_manager.ui_data
        

        layout = self.layout
        col = layout.column(align=True)

        col.prop(pk, 'armature')

        if not pk.armature:
            return

        col.prop(pk, 'picker_name')
        col.prop(pk, 'generate_picker_image')
        row = col.row()
        row.enabled = not pk.generate_picker_image
        row.prop(pk, 'picker_image')
        
        '''
        row = col.row()
        row.enabled = context.mode == 'POSE'
        row.prop(pk, 'only_selected_pose_bones')
        col.prop(pk, 'generate_default_layers')
        col.prop(pk, 'generate_picker_image')
        col.prop(pk, 'view')
        row = col.row()
        row.enabled = pk.view == 'FRONT'
        row.prop(pk, 'picker_image')
        col.prop(pk, 'generate_facial')
        _col = col.column()
        _col.enabled = pk.generate_facial
        _col.prop(pk, 'facial_views')
        row = col.row()
        row.enabled = pk.facial_views == 'FRONT'
        row.prop(pk, 'picker_facial_image')

        box = col.box().grid_flow(columns=2, row_major=True)
        box.prop(pk, 'color_hand_l')
        box.prop(pk, 'color_hand_r')
        box.prop(pk, 'color_arm_l')
        box.prop(pk, 'color_arm_r')
        box.prop(pk, 'color_leg_l')
        box.prop(pk, 'color_leg_r')
        box.prop(pk, 'color_body')
        box.prop(pk, 'color_head')
        '''

        op = layout.row()
        op.scale_y = 1.25
        op.operator('pk.create_picker', text="Create Picker")

        if len(context.scene.pickers.data) > 0:
            op = layout.row()
            op.scale_y = 1.25
            op.operator('pk.draw_picker', text="Draw Picker")
