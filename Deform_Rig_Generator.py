import bpy
from bpy_extras import anim_utils
import os

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


constraint_type = [("TRANSFORM","Copy Transform","Copy Transform"),("LOTROT","Copy Location & Copy Rotation","Lot Rot")]
ENUM_Extract_Mode = [("SELECTED","Selected","Selected"),("DEFORM","Deform","Deform"), ("SELECTED_DEFORM", "Selected Deform", "Selected Deform")]

class CGD_Generate_Game_Rig(bpy.types.Operator):
    """This will Generate a Deform Game Rig based on the step in CGDive Video"""
    bl_idname = "cgd.generate_game_rig"
    bl_label = "Generate Game Rig"
    bl_info = {'UNDO', "REGISTER"}

    Extract_Mode: bpy.props.EnumProperty(items=ENUM_Extract_Mode, default="DEFORM")
    Flat_Hierarchy: bpy.props.BoolProperty(default=False)
    Disconnect_Bone: bpy.props.BoolProperty(default=True)

    Constraint_Type: bpy.props.EnumProperty(items=constraint_type, default="LOTROT")

    Animator_Remove_BBone : bpy.props.BoolProperty(default=True)
    Animator_Disable_Deform : bpy.props.BoolProperty(default=False)

    Parent_To_Deform_Rig: bpy.props.BoolProperty(default=True)
    Deform_Armature_Name: bpy.props.StringProperty()
    Deform_Remove_BBone : bpy.props.BoolProperty(default=True)

    Deform_Move_Bone_to_Layer1 : bpy.props.BoolProperty(default=True)

    Deform_Set_Inherit_Rotation_True: bpy.props.BoolProperty(default=True)
    Deform_Set_Inherit_Scale_Full: bpy.props.BoolProperty(default=True)
    Deform_Set_Local_Location_True: bpy.props.BoolProperty(default=True)

    Deform_Remove_Non_Deform_Bone: bpy.props.BoolProperty(default=True)
    Deform_Unlock_Transform: bpy.props.BoolProperty(default=True)
    Deform_Remove_Shape: bpy.props.BoolProperty(default=True)
    Deform_Remove_All_Constraints: bpy.props.BoolProperty(default=True)
    Deform_Copy_Transform: bpy.props.BoolProperty(default=True)
    Deform_Bind_to_Deform_Rig: bpy.props.BoolProperty(default=True)

    Remove_Custom_Properties: bpy.props.BoolProperty(default=True)
    Remove_Animation_Data: bpy.props.BoolProperty(default=True)

    Show_Option: bpy.props.BoolProperty(default=False)


#    RIGIFY_Disable_Stretch: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):

        object = context.object

        self.Deform_Armature_Name = object.name + "_deform"

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):



        layout = self.layout


        layout.prop(self, "Deform_Armature_Name", text="Name")

        layout.prop(self, "Flat_Hierarchy", text="Flat Hierarchy")
        layout.prop(self, "Disconnect_Bone", text="Disconnect Bone")
        layout.prop(self, "Constraint_Type", text="Constraint Type")

        layout.prop(self, "Extract_Mode", text="Extract Mode")

        layout.prop(self, "Show_Option", text="Options")



        if self.Show_Option:

            layout.label(text="Animator Armature")
            layout.prop(self, "Animator_Remove_BBone", text="Remove BBone")


            layout.separator()

            layout.label(text="Deform Armature")
            layout.prop(self, "Deform_Remove_BBone", text="Remove BBone")
            layout.prop(self, "Deform_Move_Bone_to_Layer1", text="Move Bones to Layer 1")

            layout.prop(self, "Deform_Set_Inherit_Rotation_True", text="Set Inherit Rotation True")
            layout.prop(self, "Deform_Set_Inherit_Scale_Full", text="Set Inherit Scale Full")
            layout.prop(self, "Deform_Set_Local_Location_True", text="Set Local Location Bone Setting True")

            layout.prop(self, "Deform_Remove_Non_Deform_Bone", text="Remove Non Deform / Non Selected Bones")

            layout.prop(self, "Deform_Unlock_Transform", text="Unlock Transform")
            layout.prop(self, "Deform_Remove_Shape", text="Remove Bone Shapes")
            layout.prop(self, "Deform_Remove_All_Constraints", text="Remove Old Constraints")
            layout.prop(self, "Deform_Copy_Transform", text="Constrain Deform Rig to Animation Rig")
            layout.prop(self, "Deform_Bind_to_Deform_Rig", text="Bind to Deform Rig")
            if self.Deform_Bind_to_Deform_Rig:
                layout.prop(self, "Parent_To_Deform_Rig", text="Parent Mesh Object to Deform Rig")

            layout.prop(self, "Remove_Animation_Data", text="Remove Animation Data & Drivers")
            layout.prop(self, "Remove_Custom_Properties", text="Remove Custom Properties")

#        layout.prop(self, "RIGIFY_Disable_Stretch", text="Disable Rigify Stretch")


    def execute(self, context):



        object = context.object

        bpy.ops.object.mode_set(mode = 'OBJECT')


        if object.type == "ARMATURE":


            ORI_Edit_Bones = object.data.bones

            for bone in ORI_Edit_Bones:

                if self.Animator_Remove_BBone:
                    bone.bbone_segments = 0

#                if self.Animator_Disable_Deform:





            game_rig = object.copy()
            game_rig.display_type = "SOLID"
            game_rig.show_in_front = True
            game_rig.name = self.Deform_Armature_Name
            game_rig.data = game_rig.data.copy()
            bpy.context.collection.objects.link(game_rig)

            bpy.ops.object.select_all(action='DESELECT')
            game_rig.select_set(True)
            context.view_layer.objects.active = game_rig
            bpy.ops.object.mode_set(mode = 'EDIT')

            Edit_Bones = game_rig.data.edit_bones




            if self.Remove_Animation_Data:

                game_rig.animation_data_clear()
                game_rig.data.animation_data_clear()



            if self.Deform_Move_Bone_to_Layer1:
                for i, layer in enumerate(game_rig.data.layers):
                    if i == 0:
                        game_rig.data.layers[i] = True
                    else:
                        game_rig.data.layers[i] = False



            for bone in Edit_Bones:

                if self.Flat_Hierarchy:
                    bone.parent = None
                if self.Disconnect_Bone:
                    bone.use_connect = False

                if self.Remove_Custom_Properties:
                    if bone.get("_RNA_UI"):
                        for property in bone["_RNA_UI"]:
                            del bone[property]




                if self.Deform_Remove_BBone:
                    bone.bbone_segments = 0

                if self.Deform_Set_Inherit_Rotation_True:
                    bone.use_inherit_rotation = True

                if self.Deform_Set_Local_Location_True:
                     bone.use_local_location = True

                if self.Deform_Set_Inherit_Scale_Full:
                     bone.inherit_scale = "FULL"

                if self.Deform_Move_Bone_to_Layer1:
                    for i, layer in enumerate(bone.layers):
                        if i == 0:
                            bone.layers[i] = True
                        else:
                            bone.layers[i] = False

                if self.Deform_Remove_Non_Deform_Bone:
                    if self.Extract_Mode == "SELECTED":
                        if not bone.select:
                            Edit_Bones.remove(bone)

                    if self.Extract_Mode == "DEFORM":
                        if not bone.use_deform:
                            Edit_Bones.remove(bone)

                    if self.Extract_Mode == "SELECTED_DEFORM":
                        if not bone.select:
                            if not bone.use_deform:
                                Edit_Bones.remove(bone)


            bpy.ops.object.mode_set(mode = 'POSE')
            game_rig.data.bones.update()



            if self.Remove_Custom_Properties:
                if game_rig.get("_RNA_UI"):
                    for property in game_rig["_RNA_UI"]:
                        del game_rig[property]

                if game_rig.data.get("_RNA_UI"):
                    for property in game_rig.data["_RNA_UI"]:
                        del game_rig.data[property]

            Pose_Bones = game_rig.pose.bones

            for bone in Pose_Bones:


                if self.Remove_Custom_Properties:
                    if bone.get("_RNA_UI"):
                        for property in bone["_RNA_UI"]:
                            del bone[property]





                if self.Deform_Remove_Shape:
                    bone.custom_shape = None
                if self.Deform_Unlock_Transform:
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


                if self.Deform_Remove_All_Constraints:
                    for constraint in bone.constraints:
                        bone.constraints.remove(constraint)

                if self.Deform_Copy_Transform:

                    if self.Constraint_Type == "TRANSFORM":
                        constraint = bone.constraints.new("COPY_TRANSFORMS")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name

                    if self.Constraint_Type == "LOTROT":
                        constraint = bone.constraints.new("COPY_LOCATION")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name

                        constraint = bone.constraints.new("COPY_ROTATION")
                        constraint.target = object
                        constraint.subtarget = object.data.bones.get(bone.name).name



            bpy.ops.object.mode_set(mode = 'OBJECT')
            if self.Deform_Bind_to_Deform_Rig:
                for obj in bpy.data.objects:
                    for modifier in obj.modifiers:
                        if modifier.type == "ARMATURE":
                            if modifier.object == object:
                                modifier.object = game_rig
                                if self.Parent_To_Deform_Rig:
                                    obj.parent = game_rig
                                    obj.matrix_parent_inverse = game_rig.matrix_world.inverted()


        for bone in object.data.bones:
            if self.Animator_Disable_Deform:

                bone.use_deform = False





        return {'FINISHED'}





class CGD_Constraint_Toogle(bpy.types.Operator):

    bl_idname = "cgd.toogle_constraint"
    bl_label = "Toogle Constraints"


    mute : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if context.mode == "POSE":
            return True
        else:
            return False

    def execute(self, context):


        object = context.object
        Pose_Bone = object.pose.bones

        for bone in Pose_Bone:
            for constraint in bone.constraints:
                constraint.mute = self.mute



        return {'FINISHED'}





def draw_item(self, context):
    layout = self.layout
    row = layout.row(align=True)

    if context.mode == "POSE":
        row.operator("cgd.toogle_constraint", text="Mute Constraints").mute=True
        row.operator("cgd.toogle_constraint", text="Unmute Constraints").mute=False












class CGD_Constraint_To_Armature(bpy.types.Operator):

    bl_idname = "cgd.constraint_to_armature_name"
    bl_label = "Constraint to Armature (Name Based)"

    Armature01: bpy.props.StringProperty()
    Armature02: bpy.props.StringProperty()

    Constraint_Type: bpy.props.EnumProperty(items=constraint_type)

    def invoke(self, context, event):

        if context.object.type == "ARMATURE":
            self.Armature01 = context.object.name

        for object in context.selected_objects:
            if object.type == "ARMATURE":
                if not object == context.object:
                    self.Armature02 = object.name
                    break

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout
        layout.prop_search(self, "Armature01", bpy.data, "objects", text="Control Rig")
        layout.prop_search(self, "Armature02", bpy.data, "objects", text="Deform Rig")

        layout.prop(self, "Constraint_Type", text="Constraint Type")



    def execute(self, context):


        control_rig = bpy.data.objects.get(self.Armature01)
        deform_rig = bpy.data.objects.get(self.Armature02)

        if control_rig and deform_rig:
            if control_rig.type == "ARMATURE" and deform_rig.type == "ARMATURE":

                for bone in deform_rig.pose.bones:

                    if self.Constraint_Type == "TRANSFORM":
                        constraint = bone.constraints.new("COPY_TRANSFORMS")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name

                    if self.Constraint_Type == "LOTROT":
                        constraint = bone.constraints.new("COPY_LOCATION")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name

                        constraint = bone.constraints.new("COPY_ROTATION")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name



        return {'FINISHED'}





def draw_item(self, context):
    layout = self.layout
    row = layout.row(align=True)

    addon_preferences = context.preferences.addons[addon_name].preferences

    if context.mode == "POSE":
        if addon_preferences.toogle_constraints:
            row.operator("cgd.toogle_constraint", text="Mute Constraints").mute=True
            row.operator("cgd.toogle_constraint", text="Unmute Constraints").mute=False






class CGD_Remove_BBone(bpy.types.Operator):

    bl_idname = "cgd.remove_bbone"
    bl_label = "Remove BBone"


    def execute(self, context):

        if context.object:
            if context.object.type == "ARMATURE":
                Edit_Bones = context.object.data.bones
                for bone in Edit_Bones:
                    bone.bbone_segments = 0


        return {'FINISHED'}



class CGD_Remove_Custom_Property(bpy.types.Operator):

    bl_idname = "cgd.remove_custom_property"
    bl_label = "Remove Custom Property"

    armature: bpy.props.BoolProperty(default=True)
    object: bpy.props.BoolProperty(default=True)
    posebone: bpy.props.BoolProperty(default=True)
    editbone: bpy.props.BoolProperty(default=True)


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.object

        if object:
            if object.type == "ARMATURE":

                if self.object:
                    if object.get("_RNA_UI"):
                        for property in object["_RNA_UI"]:
                            del object[property]

                if self.armature:
                    if object.data.get("_RNA_UI"):
                        for property in object.data["_RNA_UI"]:
                            del object.data[property]



                if self.posebone:
                    Pose_Bones = object.pose.bones
                    for bone in Pose_Bones:

                        if bone.get("_RNA_UI"):
                            for property in bone["_RNA_UI"]:
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
                                del bone[property]
                    bpy.ops.object.mode_set(mode = 'OBJECT')


        return {'FINISHED'}






class CGD_Remove_Animation_Data(bpy.types.Operator):

    bl_idname = "cgd.remove_animation_data"
    bl_label = "Remove Animation Data and Drivers"


    def execute(self, context):


        if context.object:
            context.object.animation_data_clear()
            context.object.data.animation_data_clear()


        return {'FINISHED'}




class CGD_Remove_Non_Deform_Bone(bpy.types.Operator):

    bl_idname = "cgd.remove_non_deform_bone"
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





        if context.object:
            if context.object.type == "ARMATURE":
                object = context.object

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




class CGD_Remove_Bone_Shape(bpy.types.Operator):

    bl_idname = "cgd.remove_bone_shape"
    bl_label = "Remove Bone Shape"


    def execute(self, context):

        if context.object:
            if context.object.type == "ARMATURE":
                Pose_Bones = context.object.pose.bones
                for bone in Pose_Bones:
                    bone.custom_shape = None


        return {'FINISHED'}















class CGD_Constraint_Selected_Bone_To_Armature(bpy.types.Operator):

    bl_idname = "cgd.constraint_selected_bone_to_armature_name"
    bl_label = "Constraint Selected Bone to Armature (Name Based)"

    Armature01: bpy.props.StringProperty()
    Constraint_Type: bpy.props.EnumProperty(items=constraint_type)
    Clear_Constraint: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        if context.mode == "POSE":
            return True
        else:
            return False

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout

        layout.prop_search(self, "Armature01", bpy.data, "objects", text="Control Rig")
        layout.prop(self, "Constraint_Type", text="Constraint Type")
        layout.prop(self, "Clear_Constraint", text="Clear Constraints")


    def execute(self, context):


        control_rig = bpy.data.objects.get(self.Armature01)
        deform_rig = bpy.context.object

        if control_rig and deform_rig:
            if control_rig.type == "ARMATURE" and deform_rig.type == "ARMATURE":


                Selected_Pose_Bone = context.selected_pose_bones

                for bone in Selected_Pose_Bone:

                    if self.Clear_Constraint:
                        for constraint in bone.constraints:
                            bone.constraints.remove(constraint)

                    if self.Constraint_Type == "TRANSFORM":
                        constraint = bone.constraints.new("COPY_TRANSFORMS")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name

                    if self.Constraint_Type == "LOTROT":
                        constraint = bone.constraints.new("COPY_LOCATION")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name

                        constraint = bone.constraints.new("COPY_ROTATION")
                        constraint.target = control_rig
                        constraint.subtarget = control_rig.data.bones.get(bone.name).name





        return {'FINISHED'}
















class CGD_Bake_NLA_Action_Push_To_Armature(bpy.types.Operator):

    bl_idname = "cgd.bake_nla_action_push_to_armature"
    bl_label = "Bake NLA Action and Push to Armature"

    Control_Rig: bpy.props.StringProperty()
    Deform_Rig: bpy.props.StringProperty()


    Remove_Last_Keyframe: bpy.props.BoolProperty(default=False)


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        layout = self.layout

        layout.prop_search(self, "Control_Rig", bpy.data, "objects", text="Control Rig")
        layout.prop_search(self, "Deform_Rig", bpy.data, "objects", text="Deform Rig")
        layout.prop(self, "Constraint_Type", text="Constraint Type")

        layout.prop(self, "Remove_Last_Keyframe", text="Remove Last Keyframe")

    def execute(self, context):


        control_rig = bpy.data.objects.get(self.Control_Rig)
        deform_rig = bpy.data.objects.get(self.Deform_Rig)


        if control_rig and deform_rig:
            if control_rig.type == "ARMATURE" and deform_rig.type == "ARMATURE":

                if control_rig.animation_data:
                    # for nla_track in control_rig.animation_data.nla_tracks:
                    #     nla_track.mute = True

                    for nla_track in control_rig.animation_data.nla_tracks:

                        nla_track.is_solo = True

                        for strip in nla_track.strips:

                            # control_rig.animation_data.action = strip.action

                            # if not deform_rig.animation_data:
                            #     deform_rig.animation_data_create()
                            #
                            # deform_rig.animation_data.action = bpy.data.actions.new("Dummy")

                            if self.Remove_Last_Keyframe:
                                frame = [i for i in range(int(strip.action_frame_start), int(strip.action_frame_end))]

                            else:
                                frame = [i for i in range(int(strip.action_frame_start), int(strip.action_frame_end)+1)]



                            obj_act = [[deform_rig, None]]
                            Baked_Action = anim_utils.bake_action_objects(obj_act, frames=frame, only_selected=False, do_pose=True, do_object=False, do_visual_keying=True, do_constraint_clear=False, do_parents_clear=False, do_clean=False)
                            # Baked_Action[0].name = strip.action.name.replace("CTRL_", "GAME_")
                            Baked_Action[0].name = "baked_" + strip.action.name


                            deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, strip.action_frame_start, Baked_Action[0])

                    Pose_Bone = deform_rig.pose.bones
                    for bone in Pose_Bone:
                        for constraint in bone.constraints:
                            constraint.mute = True

                    # control_rig.animation_data.action = None
                    deform_rig.animation_data.action = None

                    for nla_track in control_rig.animation_data.nla_tracks:
                        nla_track.is_solo = False

                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    deform_rig.select_set(True)
                    context.view_layer.objects.active = deform_rig
        return {'FINISHED'}

















classes = [CGD_Generate_Game_Rig, CGD_Constraint_Toogle, CGD_Constraint_To_Armature, CGD_Remove_BBone, CGD_Remove_Non_Deform_Bone, CGD_Remove_Custom_Property, CGD_Remove_Animation_Data, CGD_Remove_Bone_Shape, CGD_Constraint_Selected_Bone_To_Armature, CGD_Bake_NLA_Action_Push_To_Armature]





def register():


    bpy.types.VIEW3D_HT_header.append(draw_item)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    bpy.types.VIEW3D_HT_header.remove(draw_item)
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
