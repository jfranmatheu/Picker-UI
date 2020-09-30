# Picker-UI

## Data Structure
![Hierarchical Data Structure Scheme](https://1.bp.blogspot.com/-ngqjTIPaEl0/XzpG_HWcIOI/AAAAAAAABb4/7AJ3OV8wAIo358H9g7RM8Za6SZQPyMHMACLcBGAsYHQ/s0/Anotaci%25C3%25B3n%2B2020-08-17%2B105919.png)

### PK
The root to access:
- All pickers data.
- Active picker.
- Global settings.

### PK Character
It's actually the picker. Is meant for 1 Character - 1 Picker.
- Identifier.
- Character Name.
- Target Armature.
- Active Mode.
- Scenes data.
- Transform properties.
- Theme data for style.

### PK Theme
Store sizes and colors over the picker interface, almost all is customizable.

### PK Scene
A practical use of this should be a scene for a full body picker, another one for an advanced facial picker.
- Buttons data.
- Views data.
- Active view.
 
### PK View
Meant to store different scene states/views, eg. one for front view, another one for side view.
- View name.
- Layers data.
- Button indices.
- Image.
- Image opacity.
- Mirror.
 
### PK Layer
- Button indices.
- Name.
- Icon.
- State (active...).

### PK Button
- Button data.
- Button Style.
- Name/identifier (aka bone name).
- Text.
- Index.
- Action.

### PK Button Data
- Position.
- Size.
- Factor.
- Active layer users.
- Layer users.
- Layers.
- States (selected/active/visible).

### PK Button Style
- Color.
- On Hover Color.
- Text Color.
- On Hover Text Color.
- Shape.
- Others (outline, blur, gradient...)
