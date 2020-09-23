import bpy
from bpy.types import Operator
from bpy.props import *


''' CREATE A PICKER SLOT
    pickers > data
'''
class PK_OT_create_picker(Operator):
    bl_idname = "pk.create_picker"
    bl_label = ""
    bl_description = "Create Picker"

    create_scene: BoolProperty(default=True)

    def execute(self, context):
        create = context.window_manager.ui_data

        # Create Picker and fill data
        picker = context.scene.pickers.data.add()
        picker.name = create.picker_name
        # TODO: change object to armature selector, then:
        # 1. Get object by armature name, if nothing...
        # 2. Iterate over scene objects and check for data.
        picker.arm_obj = create.armature_object
        picker.active_scene = -1 # No scenes ATM

        # Update Picker Active Index to created one
        context.scene.pickers.active_index = len(context.scene.pickers.data) - 1

        # Create Scene.
        if self.create_scene:
            scene = picker.scenes.add()
            scene.name = "Main"
            picker.active_scene = 0
            scene.active_view = 0
            if create.picker_image:
                scene.main_view.image = create.picker_image
            layer = scene.main_view.layers.add()
            layer.name = "Layer_Master"
            layer.text = "Master"
            layer.is_active = True
        return {'FINISHED'}


''' CREATE A PICKER SCENE SLOT
    active_picker > scenes
'''
class PK_OT_create_picker_scene(Operator):
    bl_idname = "pk.create_picker_scene"
    bl_label = ""
    bl_description = "Create Picker Scene"

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        create = context.window_manager.ui_data
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        # Create Scene and fill data
        pk_scene = active_picker.scenes.add()
        if create.scene_name.startswith('New Scene') and active_picker.active_scene != -1:
            create.scene_name = "New Scene__" + str(len(active_picker.scenes))
        pk_scene.name = create.scene_name
        pk_scene.active_view = 0 # NOTE: this should be 0 instead -1 as now views are pre-defined. (main and secondary, not collection anymore)
        # Update Active Scene Index to created one
        active_picker.active_scene = len(active_picker.scenes) - 1
        return {'FINISHED'}

''' CREATE A PICKER VIEW
    active_picker > active_scene > views
'''
class PK_OT_create_picker_view(Operator):
    bl_idname = "pk.create_picker_view"
    bl_label = ""
    bl_description = "Create Picker View"

    view : StringProperty(default='', name="View")
    ok_views = {'FRONT', 'RIGHT', 'LEFT', 'BACK', 'TOP'}

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        create = context.window_manager.ui_data
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            return {'CANCELLED'}
        active_scene = active_picker.scenes[active_picker.active_scene]
        # Create View and fill data
        pk_view = active_scene.views.add()
        if create.view_name.startswith('New View') and active_scene.active_view != -1:
            create.view_name = "New View__" + str(len(active_scene.views))
        pk_view.name = create.view_name
        pk_view.view = self.view if self.view != '' and self.view in self.ok_views else create.view
        # Update Active View Index to created one
        active_scene.active_view = len(active_scene.views) - 1
        return {'FINISHED'}


''' CREATE A PICKER LAYER
    active_picker > active_scene > active_view > layers
'''
class PK_OT_create_picker_layer(Operator):
    bl_idname = "pk.create_picker_layer"
    bl_label = ""
    bl_description = "Create Picker Layer"

    text : StringProperty(default='', name="Text")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        create = context.window_manager.ui_data
        pickers = context.scene.pickers
        active_picker = pickers.data[pickers.active_index]
        if active_picker.active_scene == -1:
            return {'CANCELLED'}
        active_scene = active_picker.scenes[active_picker.active_scene]
        if active_scene.active_view == -1:
            return {'CANCELLED'}
        active_view = active_scene.views[active_scene.active_view]
        # Create LAYER and fill data
        if create.layer_name.startswith('New Layer') and len(active_view.layers) > 0:
            create.layer_name = "New Layer__" + str(len(active_view.layers))
        pk_layer = active_view.layers.add()
        pk_layer.name = create.layer_name if self.text == '' else "Layer_" + self.text
        pk_layer.text = create.layer_text if self.text == '' else self.text
        pk_layer.button_indices = []
        pk_layer.button_indices_text = bpy.data.texts.new(pk_layer.name)
        pk_layer.is_active = True
        return {'FINISHED'}


''' CREATE A PICKER BUTTON SLOT
    active_picker > active_scene > buttons
'''
class PK_OT_create_picker_button(Operator):
    bl_idname = "pk.create_picker_button"
    bl_label = ""
    bl_description = "Create Picker Button"

    text : StringProperty(default='', name="Text")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        create = context.window_manager.ui_data
        active_scene = context.scene.pickers.active_scene()
        if not active_scene:
            return {'CANCELLED'}

        # Check if button is already created
        name = create.button_target_bone.name
        if active_scene.buttons.get(name, None) or not active_scene.get_active_view():
            return {'CANCELLED'}

        if self.text == '':
            if create.button_text.startswith('Text') and len(active_scene.buttons) != 0:
                create.button_text = "Text." + str(len(active_scene.buttons))
            text = create.button_text
        else:
            text = self.text

        active_scene.add_button(name, text)
        return {'FINISHED'}


''' ADD BUTTON TO SELECTED LAYER
    active_picker > active_scene > active_view > layer(INDEX)
'''
class PK_OT_add_button_to_view(Operator):
    bl_idname = "pk.add_button_to_view"
    bl_label = ""
    bl_description = "Add button to Active View"

    button_index : IntProperty(default=-1, name="Button Index")
    button_name : StringProperty(default='', name="Button Name")
    remove : BoolProperty(default=False, name="Remove Instead?")
    to_all_active_layers : BoolProperty(default=False, name="Add to all active layers of this view?")

    @classmethod
    def poll(cls, context):
        # No Pickers
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        active_scene = context.scene.pickers.active_scene()
        # No Scene
        if not active_scene:
            return {'CANCELLED'}
        # Invalid indices
        if self.button_index == -1:
            if self.button_name == '':
                return {'CANCELLED'}
            index = active_scene.buttons.get(self.button_name)
        else:
            index = self.button_index
        active_view = active_scene.get_active_view()
        # No View
        if not active_view:
            return {'CANCELLED'}
        # No buttons or invalid button.
        if len(active_view.buttons) == 0 or index > len(active_view.buttons) - 1:
            return {'CANCELLED'}

        if self.remove:
            # Button is NOT in view !
            if not active_view.check_button(index):
                return {'CANCELLED'}
            # Remove button from View:
            active_view.remove_button(index)
        else:
            # Button already in view !
            if active_view.check_button(index):
                return {'CANCELLED'}
            # Add button to View.
            active_view.add_button(index)
            # Add button to all active_layers of active_view.
            if self.to_all_active_layers:
                button_data = active_scene.buttons[index].get_data_from_view_index(active_scene.active_view)
                active_layers = active_view.active_layers()
                for layer in active_layers:
                    if not layer.check_button(index):
                        layer.add_button(index)
                        button_data.layer_users += 1
                        button_data.active_layer_users += 1
                # There's really some active view present(?)
                if active_layers:
                    button_data.is_active = True # So activate this button.
                    button_data.is_visible = True
        return {'FINISHED'}


''' REMOVE A PICKER BUTTON SLOT
    active_picker > active_scene > buttons
'''
class PK_OT_remove_picker_button(Operator):
    bl_idname = "pk.remove_picker_button"
    bl_label = ""
    bl_description = "Remove Picker Button"

    button_index : IntProperty(default=-1, name="Button Index")

    @classmethod
    def poll(cls, context):
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        if self.button_index == -1:
            return {'CANCELLED'}
        active_scene = context.scene.pickers.active_scene()
        if not active_scene:
            return {'CANCELLED'}
        active_view = active_scene.active_index()
        if not active_view or self.button_index > active_scene.buttons[-1].index: # NOTE: TAKE CARE !
            return {'CANCELLED'}
        active_scene.remove_button(self.button_index)
        return {'FINISHED'}


''' ADD BUTTON TO SELECTED LAYER
    active_picker > active_scene > active_view > layer(INDEX)
'''
class PK_OT_add_button_to_layer(Operator):
    bl_idname = "pk.add_button_to_layer"
    bl_label = ""
    bl_description = "Add button to layer"

    layer_index : IntProperty(default=-1, name="Layer Index")
    button_index : IntProperty(default=-1, name="Button Index")
    remove : BoolProperty(default=False, name="Remove Instead?")

    @classmethod
    def poll(cls, context):
        # No Pickers
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        # Invalid indices
        if self.layer_index == -1 or self.button_index == -1:
            return {'CANCELLED'}
        active_scene = context.scene.pickers.active_scene()
        # No Scene
        if not active_scene:
            return {'CANCELLED'}
        active_view = active_scene.get_active_view()
        # No View
        if not active_view:
            return {'CANCELLED'}
        # No Layers or invalid layer
        if len(active_view.layers) == 0 or self.layer_index > len(active_view.layers) - 1:
            return {'CANCELLED'}
        # No buttons or invalid button
        if len(active_view.buttons) == 0 or self.button_index > len(active_view.buttons) - 1:
            return {'CANCELLED'}
        # Button is not in active_view buttons
        if not active_view.check_button(self.button_index):
            # NOTE: We can solve this by adding to the view...
            # active_view.add_button(self.button_index)
            # and setting up layer users of the button...
            return {'CANCELLED'}

        layer = active_view.layers[self.layer_index]
        if self.remove:
            # Button doesn't exist !
            if not layer.check_button(self.button_index):
                return {'CANCELLED'}
            layer.button_indices.remove(self.button_index)
        else:
            # Button was already there !
            if layer.check_button(self.button_index):
                return {'CANCELLED'}
            layer.button_indices.append(self.button_index)
        return {'FINISHED'}


''' ADD BUTTON TO ACTIVE LAYERS
    active_picker > active_scene > active_view > active_layers
'''
class PK_OT_add_button_to_active_layers(Operator):
    bl_idname = "pk.add_button_to_active_layers"
    bl_label = ""
    bl_description = "Add button to active layers"

    button_name : StringProperty(default='', name="Button Name")
    button_index : IntProperty(default=-1, name="Button Index")
    remove : BoolProperty(default=False, name="Remove Instead?")

    @classmethod
    def poll(cls, context):
        # No Pickers
        return context.scene.pickers.active_index != -1

    def execute(self, context):
        active_scene = context.scene.pickers.active_scene()
        # No Scene
        if not active_scene:
            return {'CANCELLED'}
        # Invalid indices
        if self.button_index == -1:
            if self.button_name == '':
                return {'CANCELLED'}
            index = active_scene.buttons.get(self.button_name)
        else:
            index = self.button_index
        active_view = active_scene.get_active_view()
        # No View
        if not active_view:
            return {'CANCELLED'}
        # No buttons or invalid button.
        if len(active_view.buttons) == 0 or index > len(active_view.buttons) - 1:
            return {'CANCELLED'}

        active_layers = active_view.active_layers()
        # No active layers !
        if not active_layers:
            return {'CANCELLED'}

        button_data = active_scene.buttons[index].get_data_from_view_index(active_scene.active_view)

        if self.remove:
            # Button is NOT in view, so let's suppose is not in any layer
            if not active_view.check_button(index):
                return {'CANCELLED'}
            # Remove button from active View layers...
            num_non_active_layers_containing_button = 0
            for layer in active_view.layers:
                if layer.is_active:
                    if layer.check_button(index):
                        layer.remove_button(index)
                        button_data.layer_users -= 1
                        button_data.active_layer_users -= 1
                else:
                    # Another layer contain this button !
                    if layer.check_button(index):
                        num_non_active_layers_containing_button += 1
            # NO MORE LAYERS CONTAINS THIS BUTTON ?
            # REMOVE FROM VIEW !
            if num_non_active_layers_containing_button == 0:
                active_view.remove_button(index)
                # TODO: Check for scenes to remove from scene!
        else:
            # Button already in view !
            if active_view.check_button(index):
                return {'CANCELLED'}
            # Add button to active_layers only if it's not there.
            for layer in active_layers:
                if not layer.check_button(index):
                    layer.add_button(index)
                    button_data.layer_users += 1
                    button_data.active_layer_users += 1
            # Ensure button is active if it's inside an active_layer
            if active_layers:
                button_data.is_active = True
                button_data.is_visible = True
        return {'FINISHED'}
