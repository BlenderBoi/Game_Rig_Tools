
import bpy

class GRT_Remove_Non_Deform_Bone(bpy.types.Operator):

    bl_idname = "gamerigtool.remove_non_deform_bone"
    bl_label = "Remove Non Deform Bone"

    move_bone_to_layer_1: bpy.props.BoolProperty(default=True)
    remove_constraints: bpy.props.BoolProperty(default=True)
    unlock_transform: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "move_bone_to_layer_1", text="Move Bones to Layer 1")
        layout.prop(self, "remove_constraints", text="Clear Constraints")
        layout.prop(self, "unlock_transform", text="Unlock Transform")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):


        for object in context.selected_objects:

            if object:
                if object.type == "ARMATURE":
                    object = object

                    bpy.ops.object.select_all(action='DESELECT')
                    object.select_set(True)
                    context.view_layer.objects.active = object


                    bpy.ops.object.mode_set(mode = 'EDIT')
                    Edit_Bones = object.data.edit_bones
                    for bone in Edit_Bones:

                        if self.move_bone_to_layer_1:
                            for i, layer in enumerate(bone.layers):
                                if i == 0:
                                    bone.layers[i] = True
                                else:
                                    bone.layers[i] = False

                        if not bone.use_deform:
                            Edit_Bones.remove(bone)







                bpy.ops.object.mode_set(mode = 'OBJECT')

                # Pose_Bones = object.pose.bones
                #
                # for bone in Pose_Bones:
                #     if self.move_bone_to_layer_1:
                #         for i, layer in enumerate(bone.layers):
                #             if i == 0:
                #                 bone.layers[i] = True
                #             else:
                #                 bone.layers[i] = False


                if self.move_bone_to_layer_1:
                    for i, layer in enumerate(object.data.layers):
                        if i == 0:
                            object.data.layers[i] = True
                        else:
                            object.data.layers[i] = False






                Pose_Bones = object.pose.bones

                for bone in Pose_Bones:

                    if self.unlock_transform:
                        bone.lock_location[0] = False
                        bone.lock_location[1] = False
                        bone.lock_location[2] = False

                        bone.lock_scale[0] = False
                        bone.lock_scale[1] = False
                        bone.lock_scale[2] = False

                        bone.lock_rotation_w = False
                        bone.lock_rotation[0] = False
                        bone.lock_rotation[1] = False
                        bone.lock_rotation[2] = False

                    if self.remove_constraints:
                        for constraint in bone.constraints:
                            bone.constraints.remove(constraint)


        return {'FINISHED'}


classes = [GRT_Remove_Non_Deform_Bone]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
