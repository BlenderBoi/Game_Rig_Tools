import bpy



Mode = [("REPLACE","Replace","Replace"),("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix")]

class GRT_Batch_Rename_Actions(bpy.types.Operator):

    bl_idname = "gamerigtool.batch_rename_actions"
    bl_label = "Batch Rename Actions"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(items=Mode)
    name_01: bpy.props.StringProperty()
    name_02: bpy.props.StringProperty()




    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):

        layout = self.layout
        layout.prop(self, "mode", text="Mode")

        if self.mode == "REPLACE":
            layout.prop(self, "name_01", text="From")
            layout.prop(self, "name_02", text="To")

        if self.mode == "PREFIX":
            layout.prop(self, "name_01", text="Prefix")

        if self.mode == "SUFFIX":
            layout.prop(self, "name_01", text="Suffix")



    def execute(self, context):

        actions = bpy.data.actions

        bpy.context.view_layer.update()

        for action in actions:

            if self.mode == "PREFIX":
                name = self.name_01 + action.name
                action.name = name

            if self.mode == "SUFFIX":
                name = action.name + self.name_01
                action.name = name

            if self.mode == "REPLACE":
                action.name = action.name.replace(self.name_01, self.name_02)


        return {'FINISHED'}




classes = [GRT_Batch_Rename_Actions]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
