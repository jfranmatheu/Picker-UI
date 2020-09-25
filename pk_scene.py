from bpy.types import PropertyGroup
from bpy.props import (
    CollectionProperty, IntProperty, PointerProperty, StringProperty
)
from .pk_button import PK_Button
from .pk_view import PK_View


MASTER_VIEW = 0
SECONDARY_VIEW = 1


class PK_Scene(PropertyGroup):
    name : StringProperty(default="Scene_", name="Name")
    #gr_buttons : CollectionProperty(type=PK_Button_Graphics, name="Buttons")
    buttons : CollectionProperty(type=PK_Button, name="Buttons")

    # NOTE: layers are not part of scene anymore but of each view
    # to prevent button_indices issues and conflicts between different views.
    # layers : CollectionProperty(type=PK_Layer, name="Layers")

    ''' We should save different positions and/or sizes per view for buttons:
        MODEL 1:
            Store Transforms and active state inside a collection in PK_Buttons,
            the view index (active_view) should be the same for this transform col. index.
            Pros: no problems with different indices between gr_button and view button as
            is an all-in-one data block. Better access. No overhelming.
            Deleting buttons is easier, don't need to iter view buttons.
            Cons: have to iter over all buttons but could be improved with chached list
            on each view/layer. Deleting a layer suppose to iter over buttons
            to delete the corresponding view index in button.data[view_index].
            Manage buttons as view buttons is a pain as we need to know the indices.
            NOTE BIG ISSUE: Need to create button_data for ALL buttons when creating a view,
            even if 90% of buttons is not in that view (memory consumer).
        MODEL 2:
            Otherwise, store them inside each view as a 'buttons' collection.
            The pros are removing a view will remove all that data too,
            so no need to iter each scene button. Also, no need to iter all buttons,
            just view buttons so it's much cheaper.
            The cons are we have to save the index of the gr_button inside the button data
            and when removing the gr_button (all button) we have to iter for all view buttons
            to delete view buttons, BUT we don't have a way to know the indices in that direction,
            is not bidirectional, we can know gr_button index inside view button, but not in the
            other direction, NOTE SOLUTION: We can't delete gr_button, we just delete view button,
            when all view buttons are deleted (something like view_buttons_users inside gr_button),
            then gr_button is removed completely...
        MODEL 3: NOTE: I picked this one.
            Just keep 2 views per scene: master view, secondary view.
            - We can store 2 position for buttons: pos1, pos2. -> depending view
            - We need some active_view min=0, max=1 or boolean. MASTER_VIEW = 0; SECONDARY_VIEW = 1.
            - We need a list of button indices inside each view, we will use this as a cache.
            - We need some bool[2] active_view per button to know if button is visible/active
                in that view, so we can fill the button_indices list (our cache) with all this.
            - No gr_button and view.button separated, it's an all-in-one data-block part of scene.
    '''
    #views : CollectionProperty(type=PK_View, name="Views")
    main_view : PointerProperty(type=PK_View, name="Master View")
    secondary_view : PointerProperty(type=PK_View, name="Secondary View")
    active_view : IntProperty(default=-1, name="Active View")

    # TEMPORAL PROPERTIES
    # TODO: reset this or make it temporal.
    active_button : IntProperty(default=-1, name="Active Button")

    def get_active_button(self): # TODO: check if index is correct(?).
        return None if self.active_button == -1 else self.buttons[self.active_button]

    def get_active_view(self):
        #return views[view_index] if active_view != -1 else None
        return self.main_view if self.active_view == MASTER_VIEW \
            else self.secondary_view if self.active_view == SECONDARY_VIEW \
            else None

    def other_view(self):
        #return views[view_index] if active_view != -1 else None
        return self.secondary_view if self.active_view == MASTER_VIEW \
            else self.main_view if self.active_view == SECONDARY_VIEW \
            else None

    def add_button(self, name, text):
        # Create button
        pk_button = self.buttons.add()
        pk_button.name = name # MUST BE the bone name
        pk_button.index = len(self.buttons) - 1
        pk_button.style.text = text
        pk_button.get_data_from_view_index(self.active_view).init_default()
        # Add button to active view
        self.get_active_view().add_button(pk_button)

    def print_button(self):
        print("[%s] Button Indices:" % self.name)
        for b in self.buttons:
            print("\t- %s - %i" % (b.name, b.index))

    def remove_button(self, button, skip_views=False):
        self.print_button()
        idx = button if isinstance(button, int) else button.index
        print("Button %s with index %i was removed." % (button.name, idx))
        self.buttons.remove(idx)
        if not skip_views:
            self.main_view.remove_button(idx)
            self.secondary_view.remove_button(idx)
        self.update_indices(idx)
        self.print_button()

    def update_indices(self, from_index=0):
        buttons_to_update = []
        for idx in range(from_index, len(self.buttons)):
            buttons_to_update.append(self.buttons[idx].index)
            self.buttons[idx].index = idx
        if not buttons_to_update:
            return None
        # If removed button was in this view, then update view indices
        if self.main_view.check_button(from_index):
            self.main_view.update_indices(buttons_to_update)
        if self.secondary_view.check_button(from_index):
            self.secondary_view.update_indices(buttons_to_update)

    def is_selected(self, button) -> bool:
        return self.buttons[button].is_selected[self.active_view] if isinstance(button, int) else button.is_selected[self.active_view]

    def is_active(self, button) -> bool:
        return self.buttons[button].is_active[self.active_view] if isinstance(button, int) else button.is_active[self.active_view]

    def is_visible(self, button) -> bool:
        return self.buttons[button].is_visible[self.active_view] if isinstance(button, int) else button.is_visible[self.active_view]
    