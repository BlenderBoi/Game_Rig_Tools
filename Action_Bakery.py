import bpy
from bpy_extras import anim_utils



class CGD_UL_Action_Bakery_List(bpy.types.UIList):


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scn = context.scene
        ob = data
        row = layout.row(align=True)


        row.prop(item, "bake_checkbox", text="", emboss=True)
        row.prop(item, "name", text="", emboss=False)

        row = layout.row(align=True)
        row.alignment = "RIGHT"
        row.prop(item, "loop", text="Loop", emboss=True)





ENUM_name_addon = [("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix"),("REPLACE","Replace","Replace")]


class CGD_Bake_Action_Bakery(bpy.types.Operator):

    bl_idname = "cgd.bake_action_bakery"
    bl_label = "Bake Action Bakery"
    bl_info = {'UNDO', "REGISTER"}


    Mode: bpy.props.EnumProperty(items=ENUM_name_addon,default="REPLACE")
    TEXT01: bpy.props.StringProperty(default="CTRL_")
    TEXT02: bpy.props.StringProperty(default="")


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Mode", text="Mode")

        if self.Mode == "PREFIX":
            layout.prop(self, "TEXT01", text="Prefix")
        if self.Mode == "SUFFIX":
            layout.prop(self, "TEXT01", text="Suffix")
        if self.Mode == "REPLACE":
            layout.prop(self, "TEXT01", text="From")
            layout.prop(self, "TEXT02", text="To")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):


        scn = context.scene

        control_rig = scn.bake_control_armature
        deform_rig = scn.bake_deform_armature


        if control_rig and deform_rig:
            if control_rig.type == "ARMATURE" and deform_rig.type == "ARMATURE":

                if control_rig.animation_data:

                    for nla_track in control_rig.animation_data.nla_tracks:
                        nla_track.is_solo = False

                    if deform_rig.animation_data:
                        for nla_track in deform_rig.animation_data.nla_tracks:
                            nla_track.is_solo = False

                    if scn.Unmute_Before_Bake:
                        Pose_Bone = deform_rig.pose.bones
                        for bone in Pose_Bone:
                            for constraint in bone.constraints:
                                constraint.mute = False


                    for action in bpy.data.actions:

                        if action.bake_checkbox:
                            control_rig.animation_data.action = action

                            if action.loop:
                                frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1]))]

                            else:
                                frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1])+1)]


                            obj_act = [[deform_rig, None]]
                            Baked_Action = anim_utils.bake_action_objects(obj_act, frames=frame, only_selected=False, do_pose=True, do_object=False, do_visual_keying=True, do_constraint_clear=False, do_parents_clear=False, do_clean=False)

                            if self.Mode == "REPLACE":
                                action_name = action.name.replace(self.TEXT01, self.TEXT02)
                            if self.Mode == "PREFIX":
                                action_name = self.TEXT01 + action.name
                            if self.Mode == "SUFFIX":
                                action_name =  action.name + self.TEXT01

                            Baked_Action[0].name = action_name

                            if scn.Push_to_NLA:
                                deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, action.frame_range[0], Baked_Action[0])


                    if scn.Mute_After_Bake:
                        Pose_Bone = deform_rig.pose.bones
                        for bone in Pose_Bone:
                            for constraint in bone.constraints:
                                constraint.mute = True

                    control_rig.animation_data.action = None
                    deform_rig.animation_data.action = None



                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    deform_rig.select_set(True)
                    context.view_layer.objects.active = deform_rig



        return {'FINISHED'}






















classes = (
        CGD_UL_Action_Bakery_List,
        CGD_Bake_Action_Bakery
        )























def armature_poll(self, object):
    return object.type == 'ARMATURE'






def register():



    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.action_bakery_index = bpy.props.IntProperty()

    bpy.types.Action.use_custom_range = bpy.props.BoolProperty(default=False)

    bpy.types.Action.custom_range_start = bpy.props.IntProperty()
    bpy.types.Action.custom_range_end = bpy.props.IntProperty()

    bpy.types.Action.loop = bpy.props.BoolProperty(default=False)
    bpy.types.Action.bake_checkbox = bpy.props.BoolProperty(default=False)

    bpy.types.Scene.bake_deform_armature = bpy.props.PointerProperty(type=bpy.types.Object, poll=armature_poll)
    bpy.types.Scene.bake_control_armature = bpy.props.PointerProperty(type=bpy.types.Object, poll=armature_poll)
    bpy.types.Scene.Push_to_NLA = bpy.props.BoolProperty(default=True)

    bpy.types.Scene.Unmute_Before_Bake= bpy.props.BoolProperty(default=True)
    bpy.types.Scene.Mute_After_Bake= bpy.props.BoolProperty(default=True)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.action_bakery_index

    del bpy.types.Action.use_custom_range

    del bpy.types.Action.custom_range_start
    del bpy.types.Action.custom_range_end

    del bpy.types.Action.loop
    del bpy.types.Action.bake_checkbox

    del bpy.Scene.Action.bake_deform_armature
    del bpy.Scene.Action.bake_control_armature
    del bpy.Scene.Action.Push_to_NLA

    del bpy.types.Scene.Unmute_Before_Bake
    del bpy.types.Scene.Mute_After_Bake


if __name__ == "__main__":
    register()
