import bpy
from .. import Utility

class GRT_Remove_Custom_Property(bpy.types.Operator):

    bl_idname = "gamerigtool.remove_custom_property"
    bl_label = "Remove Custom Property"
    bl_options = {'REGISTER', 'UNDO'}

    data: bpy.props.BoolProperty(default=True)
    object: bpy.props.BoolProperty(default=True)
    posebone: bpy.props.BoolProperty(default=True)
    editbone: bpy.props.BoolProperty(default=True)

    #Only Armature Object

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "data", text="Data")
        layout.prop(self, "object", text="Object")

        Armature_Objects = [object for object in context.selected_objects if object.type == "ARMATURE"]

        if len(Armature_Objects) > 0:

            layout.prop(self, "posebone", text="Pose Bone")
            layout.prop(self, "editbone", text="Edit Bone")



    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.object
        context.view_layer.update()

        for object in context.selected_objects:

            if object:

                if self.object:
                    if object.get("_RNA_UI"):
                        for property in object["_RNA_UI"]:
                            if object.get(property):
                                del object[property]

                if self.data:
                    if object.data.get("_RNA_UI"):
                        for property in object.data["_RNA_UI"]:
                            if object.data.get(property):
                                del object.data[property]


                if object.type == "ARMATURE":

                    if self.posebone:
                        Pose_Bones = object.pose.bones

                        for bone in Pose_Bones:

                            if bone.get("_RNA_UI"):
                                for property in bone["_RNA_UI"]:

                                    if bone.get(property):
                                        del bone[property]

                    if self.editbone:

                        bpy.ops.object.select_all(action='DESELECT')
                        object.select_set(True)
                        context.view_layer.objects.active = object

                        bpy.ops.object.mode_set(mode = 'EDIT')
                        Edit_Bones = object.data.edit_bones
                        for bone in Edit_Bones:

                            if bone.get("_RNA_UI"):
                                for property in bone["_RNA_UI"]:

                                    if bone.get(property):
                                        del bone[property]
                        bpy.ops.object.mode_set(mode = 'OBJECT')

        context.view_layer.update()
        Utility.update_UI()
        return {'FINISHED'}


classes = [GRT_Remove_Custom_Property]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
