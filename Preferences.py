import bpy


class CGD_user_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    side_panel: bpy.props.BoolProperty(default=True)
    armature_data: bpy.props.BoolProperty(default=False)

    show_tool: bpy.props.BoolProperty(default=False)
    show_action_bakery: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "side_panel", text="Show in Side Panel")
        layout.prop(self, "armature_data", text="Show in Data Properties")

classes = [CGD_user_preferences]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)





def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
