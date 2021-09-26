import bpy
from . import Utility
import os
from bpy_extras import anim_utils


script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)



ENUM_list_operation = [("ADD","Add","Add"),("REMOVE","Remove","Remove"),("UP","Up","Up"), ("DOWN","Down","Down"),("ASSIGN","Assign","Assign"),("UNASSIGN","Unassign","Unassign"), ("LOAD_ALL_ACTIONS", "Load All Actions", "Load All Actions"), ("LOAD_ACTIVE_ACTIONS", "Load Active Actions", "Load Active Actions")]

class GRT_Action_Bakery_List_Operator(bpy.types.Operator):
    """List Operator"""
    bl_idname = "gamerigtool.action_bakery_list_operator"
    bl_label = "List Operator"
    bl_options = {'UNDO', 'REGISTER'}

    operation: bpy.props.EnumProperty(items=ENUM_list_operation)
    action: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    assign: bpy.props.BoolProperty(default=True)


    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "action", bpy.data, "actions" ,text="Action")

    def invoke(self, context, event):

        if self.operation == "ADD":
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):


        scn = context.scene
        item_list = scn.GRT_Action_Bakery
        item_index = self.index

        # if len(item_list) > 0:
        #
        #     for item in item_list:
        #         for index, action in enumerate(item_list):
        #             if not item.Action:
        #                 item_list.remove(index)
        #                 break

        if self.operation == "LOAD_ACTIVE_ACTIONS":

            object = context.object
            if object:
                if object.type == "ARMATURE":
                    action = None

                    if object.animation_data:
                        if object.animation_data.action:
                            action = object.animation_data.action

                    if action:

                        check = [item.Action for item in item_list]

                        if not action in check:
                            item = item_list.add()
                            item.Action = action

                            scn.GRT_Action_Bakery_Index = len(item_list) - 1

            Utility.update_UI()

            return {'FINISHED'}


        if self.operation == "LOAD_ALL_ACTIONS":

            for action in bpy.data.actions:

                check = [item.Action for item in item_list]

                if not action in check:
                    item = item_list.add()
                    item.Action = action

                    scn.GRT_Action_Bakery_Index = len(item_list) - 1

            Utility.update_UI()

            return {'FINISHED'}


        if self.operation == "REMOVE":

            item_list.remove(self.index)

            if len(item_list) == scn.GRT_Action_Bakery_Index:
                scn.GRT_Action_Bakery_Index = len(item_list) - 1
            Utility.update_UI()
            return {'FINISHED'}

        if self.operation == "ADD":

            Action = bpy.data.actions.get(self.action)

            if Action:
                item = item_list.add()
                item.Action = bpy.data.actions.get(self.action)

                scn.GRT_Action_Bakery_Index = len(item_list) - 1

                Utility.update_UI()

            return {'FINISHED'}

        if self.operation == "UP":
            if item_index >= 1:
                item_list.move(item_index, item_index-1)
                scn.GRT_Action_Bakery_Index -= 1
                return {'FINISHED'}

        if self.operation == "DOWN":
            if len(item_list)-1 > item_index:
                item_list.move(item_index, item_index+1)
                scn.GRT_Action_Bakery_Index += 1
                return {'FINISHED'}

        Utility.update_UI()
        return {'FINISHED'}

class GRT_UL_Action_Bakery_List(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scn = context.scene
        ob = data
        row = layout.row(align=True)

        Action = item.Action

        if Action:
            row.prop(item, "Bake_Select", text="")
            # row.prop(item, "Action", text="", emboss=False)
            row.prop(Action, "name", text="", emboss=False, icon="ACTION")
        else:
            row.label(text="Missing Action", icon="ERROR")

        Operator = row.operator("gamerigtool.action_bakery_list_operator", text="", icon="X")
        Operator.operation = "REMOVE"
        Operator.index = index

            # row.prop(Action, "name", text="")

class GRT_PT_Action_Bakery(bpy.types.Panel):

    bl_label = "Action Bakery"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Game Rig Tools"

    @classmethod
    def poll(cls, context):

        #Top Bar Toogle Constraint Update

        addon_preferences = context.preferences.addons[addon_name].preferences

        if addon_preferences.side_panel:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout

        scn = context.scene


        row = layout.row(align=True)
        col2 = row.column(align=True)
        col2.template_list("GRT_UL_Action_Bakery_List", "", scn, "GRT_Action_Bakery", scn, "GRT_Action_Bakery_Index")

        col = row.column(align=True)

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="ADD")
        Operator.operation = "ADD"
        Operator.index = scn.GRT_Action_Bakery_Index

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="REMOVE")
        Operator.operation = "REMOVE"
        Operator.index = scn.GRT_Action_Bakery_Index

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="TRIA_UP")
        Operator.operation = "UP"
        Operator.index = scn.GRT_Action_Bakery_Index

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="TRIA_DOWN")
        Operator.operation = "DOWN"
        Operator.index = scn.GRT_Action_Bakery_Index

        row2 = col2.row(align=True)
        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="All Action", icon="IMPORT")
        Operator.operation = "LOAD_ALL_ACTIONS"

        object = context.object
        if object:
            if object.type == "ARMATURE":
                if object.animation_data:
                    if object.animation_data.action:

                        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="Active", icon="IMPORT")
                        Operator.operation = "LOAD_ACTIVE_ACTIONS"

        Global_Settings = scn.GRT_Action_Bakery_Global_Settings

        if len(scn.GRT_Action_Bakery) > 0:
            if scn.GRT_Action_Bakery_Index < len(scn.GRT_Action_Bakery):

                active_baker = context.scene.GRT_Action_Bakery[scn.GRT_Action_Bakery_Index]

                col2.prop(active_baker, "Action", text="")



                # layout.separator()
                #
                # col = layout.column(align=True)
                # col.label(text="Control Rig")
                # col.prop(Global_Settings, "Source_Armature", text="")
                # col.label(text="Game Rig")
                # col.prop(Global_Settings, "Target_Armature", text="")
                # col.prop(Global_Settings, "Bake_Popup", text="Use Operator Popup")

                layout.prop(active_baker, "use_Local_Name", text="Use Local Name")

                if active_baker.use_Local_Name:
                    layout.prop(active_baker, "LOCAL_Baked_Name", text="")

                layout.separator()



                col = layout.column(align=True)
                col.label(text="Control Rig")
                col.prop(Global_Settings, "Source_Armature", text="")
                col.label(text="Game Rig")
                col.prop(Global_Settings, "Target_Armature", text="")

                layout.separator()


                if not Global_Settings.Source_Armature:
                    layout.label(text="Select Control Rig", icon="INFO")
                if not Global_Settings.Target_Armature:
                    layout.label(text="Select Game Rig", icon="INFO")



                row = layout.row(align=True)
                row.operator("gamerigtool.bake_action_bakery")
                row.prop(Global_Settings, "Bake_Popup", text="", icon="SETTINGS")

                layout.prop(Global_Settings, "Overwrite", text="Overwrite")
                # if Global_Settings.Overwrite:
                #     layout.prop(Global_Settings, "Clean_Empty_NLA_Strip", text="Clean Empty NLA Strip")

                layout.prop(Global_Settings, "Push_to_NLA", text="Push To NLA")

                layout.separator()

                # if Utility.draw_subpanel(active_baker, active_baker.SHOW_Local_Settings, "SHOW_Local_Settings", "Local Bake Settings", layout):


        if Utility.draw_subpanel(Global_Settings, Global_Settings.SHOW_Bake_Settings, "SHOW_Bake_Settings", "Global Bake Settings", layout):

            draw_global_bake_settings(layout, context)


def draw_global_bake_settings(layout, context):

    scn = context.scene
    Global_Settings = scn.GRT_Action_Bakery_Global_Settings






    col = layout.column(align=True)

    col.label(text="Baked Name")

    row = col.row(align=True)
    row.prop(Global_Settings, "GLOBAL_Baked_Name_Mode", expand=True)

    if Global_Settings.GLOBAL_Baked_Name_Mode == "SUFFIX":
        col.prop(Global_Settings, "GLOBAL_Baked_Name_01", text="Suffix")

    if Global_Settings.GLOBAL_Baked_Name_Mode == "PREFIX":
        col.prop(Global_Settings, "GLOBAL_Baked_Name_01", text="Prefix")

    if Global_Settings.GLOBAL_Baked_Name_Mode == "REPLACE":
        col.prop(Global_Settings, "GLOBAL_Baked_Name_01", text="From")
        col.prop(Global_Settings, "GLOBAL_Baked_Name_02", text="To")

    layout.separator()

    layout.label(text="Trim End")
    row = layout.row(align=True)
    row.prop(Global_Settings, "GLOBAL_Trim_End_Frame", text="")

    layout.separator()

    layout.label(text="Settings")

    layout.prop(Global_Settings, "Pre_Unmute_Constraint", text="Unmute Constraint Before Bake")
    layout.prop(Global_Settings, "Post_Mute_Constraint", text="Mute Constraint After Bake")

    layout.separator()

    layout.label(text="Bake Settings")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Only_Selected", text="Only Selected")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Pose", text="Do Pose")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Object", text="Do Object")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Visual_Keying", text="Do Visual Keying")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Constraint_Clear", text="Do Constraint Clear")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Parent_Clear", text="Do Parent Clear")
    layout.prop(Global_Settings, "BAKE_SETTINGS_Do_Clean", text="Do Clean")












def POLL_Armature(self, object):
    return object.type == "ARMATURE"


ENUM_Trim_Type = [("KEYFRAME","Keyframe","Keyframe"),("NLA_STRIP","NLA Strip","NLA Strip")]

class GRT_Action_Bakery_Property_Group(bpy.types.PropertyGroup):

    Action : bpy.props.PointerProperty(name="Action", type=bpy.types.Action)
    Bake_Select: bpy.props.BoolProperty(default=True)

    SHOW_Local_Settings: bpy.props.BoolProperty(default=False)

    use_Local_Name: bpy.props.BoolProperty()
    LOCAL_Baked_Name: bpy.props.StringProperty()





ENUM_Baked_Name_Mode = [("SUFFIX","Suffix","Suffix"),("PREFIX","Prefix","Prefix"),("REPLACE","Replace","Replace")]

class GRT_Action_Bakery_Global_Settings_Property_Group(bpy.types.PropertyGroup):

    Push_to_NLA: bpy.props.BoolProperty(default=True)
    Pre_Unmute_Constraint: bpy.props.BoolProperty(default=True)
    Post_Mute_Constraint: bpy.props.BoolProperty(default=True)

    GLOBAL_Baked_Name_Mode: bpy.props.EnumProperty(items=ENUM_Baked_Name_Mode)
    GLOBAL_Baked_Name_01: bpy.props.StringProperty()
    GLOBAL_Baked_Name_02: bpy.props.StringProperty()

    Overwrite: bpy.props.BoolProperty()
    Clean_Empty_NLA_Strip: bpy.props.BoolProperty(default=True)

    GLOBAL_Trim_End_Frame: bpy.props.IntProperty(min=0)


    SHOW_Bake_Settings: bpy.props.BoolProperty(default=False)

    Source_Armature: bpy.props.PointerProperty(name="Control Armature", type=bpy.types.Object, poll=POLL_Armature)
    Target_Armature: bpy.props.PointerProperty(name="Deform Armature", type=bpy.types.Object, poll=POLL_Armature)

    Bake_Popup: bpy.props.BoolProperty(default=True)

    BAKE_SETTINGS_Only_Selected: bpy.props.BoolProperty(default=False)
    BAKE_SETTINGS_Do_Pose: bpy.props.BoolProperty(default=True)
    BAKE_SETTINGS_Do_Object: bpy.props.BoolProperty(default=False)
    BAKE_SETTINGS_Do_Visual_Keying: bpy.props.BoolProperty(default=True)
    BAKE_SETTINGS_Do_Constraint_Clear: bpy.props.BoolProperty(default=False)
    BAKE_SETTINGS_Do_Parent_Clear: bpy.props.BoolProperty(default=False)
    BAKE_SETTINGS_Do_Clean: bpy.props.BoolProperty(default=False)






















class GRT_Bake_Action_Bakery(bpy.types.Operator):

    bl_idname = "gamerigtool.bake_action_bakery"
    bl_label = "Bake Action Bakery"
    bl_info = {'UNDO', "REGISTER"}

    @classmethod
    def poll(cls, context):

        scn = context.scene

        Global_Settings = scn.GRT_Action_Bakery_Global_Settings

        if Global_Settings.Source_Armature and Global_Settings.Target_Armature:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        draw_global_bake_settings(layout, context)

    def invoke(self, context, event):

        scn = context.scene
        Global_Settings = scn.GRT_Action_Bakery_Global_Settings

        if Global_Settings.Bake_Popup:

            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):

        scn = context.scene

        Global_Settings = scn.GRT_Action_Bakery_Global_Settings
        Action_Bakery = scn.GRT_Action_Bakery

        control_rig = Global_Settings.Source_Armature
        deform_rig = Global_Settings.Target_Armature


        NLA_Strip_Check = []

        CTRL_Save_Use_NLA = None
        DEF_Save_Use_NLA = None

        if control_rig.animation_data:

            CTRL_Save_Use_NLA = control_rig.animation_data.use_nla
            control_rig.animation_data.use_nla = False

        if deform_rig.animation_data:

            DEF_Save_Use_NLA = deform_rig.animation_data.use_nla
            deform_rig.animation_data.use_nla = False

        if control_rig and deform_rig:



            if control_rig.type == "ARMATURE" and deform_rig.type == "ARMATURE":

                Control_Rig_Action_Save = None

                for Baker in Action_Bakery:



                    if control_rig.animation_data:

                        # CTRL_Save_Use_NLA = control_rig.animation_data.use_nla
                        # DEF_Save_Use_NLA = deform_rig.animation_data.use_nla

                        # control_rig.animation_data.use_nla = False
                        # deform_rig.animation_data.use_nla = False

                        # for nla_track in control_rig.animation_data.nla_tracks:
                        #     nla_track.is_solo = False
                        #
                        # if deform_rig.animation_data:
                        #     for nla_track in deform_rig.animation_data.nla_tracks:
                        #         nla_track.is_solo = False

                        if Global_Settings.Pre_Unmute_Constraint:
                            Pose_Bone = deform_rig.pose.bones
                            for bone in Pose_Bone:
                                for constraint in bone.constraints:
                                    constraint.mute = False


                        if Baker.Action:
                            if Baker.Bake_Select:

                                action = Baker.Action

                                # for nla_track in control_rig.animation_data.nla_tracks:
                                #     nla_track.mute = True

                                control_rig.animation_data.action = action





                                if Baker.use_Local_Name:
                                    if Baker.LOCAL_Baked_Name:
                                        action_name = Baker.LOCAL_Baked_Name
                                    else:
                                        action_name = "Baked_" + action.name

                                else:

                                    if Global_Settings.GLOBAL_Baked_Name_Mode == "REPLACE":
                                        action_name = action.name.replace(Global_Settings.GLOBAL_Baked_Name_01, Global_Settings.GLOBAL_Baked_Name_02)
                                    if Global_Settings.GLOBAL_Baked_Name_Mode == "PREFIX":
                                        action_name = Global_Settings.GLOBAL_Baked_Name_01 + action.name
                                    if Global_Settings.GLOBAL_Baked_Name_Mode == "SUFFIX":
                                        action_name =  action.name + Global_Settings.GLOBAL_Baked_Name_01



                                frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1])+1-Global_Settings.GLOBAL_Trim_End_Frame)]

                                if Global_Settings.Overwrite:
                                    obj_act = [[deform_rig, bpy.data.actions.get(action_name)]]
                                else:
                                    obj_act = [[deform_rig, None]]

                                # obj_act = [[deform_rig, None]]
                                Baked_Action = anim_utils.bake_action_objects(obj_act, frames=frame, only_selected=Global_Settings.BAKE_SETTINGS_Only_Selected, do_pose=Global_Settings.BAKE_SETTINGS_Do_Pose, do_object=Global_Settings.BAKE_SETTINGS_Do_Object, do_visual_keying=Global_Settings.BAKE_SETTINGS_Do_Visual_Keying, do_constraint_clear=Global_Settings.BAKE_SETTINGS_Do_Constraint_Clear, do_parents_clear=Global_Settings.BAKE_SETTINGS_Do_Parent_Clear, do_clean=Global_Settings.BAKE_SETTINGS_Do_Clean)



                                # if Global_Settings.Overwrite:
                                #     duplicate_check = bpy.data.actions.get(action_name)
                                #     if duplicate_check:
                                #
                                #
                                #         context.view_layer.update()
                                #         bpy.data.actions.remove(duplicate_check)
                                #         context.view_layer.update()
                                #
                                #         if Global_Settings.Clean_Empty_NLA_Strip:
                                #             for nla_track in deform_rig.animation_data.nla_tracks:
                                #                 for s in nla_track.strips:
                                #                     for strip in nla_track.strips:
                                #                         if strip.action == None:
                                #                             nla_track.strips.remove(strip)
                                #                             break

                                Baked_Action[0].name = action_name

                                if Global_Settings.Push_to_NLA:
                                    deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, action.frame_range[0], Baked_Action[0])


                        # for nla_track_pair in nla_track_state:
                        #     print(nla_track_pair[1])
                        #     nla_track_pair[0].mute = nla_track_pair[1]

                        if Global_Settings.Post_Mute_Constraint:
                            Pose_Bone = deform_rig.pose.bones
                            for bone in Pose_Bone:
                                for constraint in bone.constraints:
                                    constraint.mute = True

                        if control_rig.animation_data:
                            if control_rig.animation_data.action:
                                control_rig.animation_data.action = None

                        if deform_rig.animation_data:
                            if deform_rig.animation_data.action:
                                deform_rig.animation_data.action = None

                        # control_rig.animation_data.use_nla = CTRL_Save_Use_NLA
                        # deform_rig.animation_data.use_nla = DEF_Save_Use_NLA


                        bpy.ops.object.mode_set(mode = 'OBJECT')
                        bpy.ops.object.select_all(action='DESELECT')
                        deform_rig.select_set(True)
                        context.view_layer.objects.active = deform_rig



        if control_rig.animation_data:

            if CTRL_Save_Use_NLA is not None:
                control_rig.animation_data.use_nla = CTRL_Save_Use_NLA

        if deform_rig.animation_data:

            if DEF_Save_Use_NLA is not None:
                deform_rig.animation_data.use_nla = DEF_Save_Use_NLA



        return {'FINISHED'}





























classes = [GRT_Bake_Action_Bakery, GRT_Action_Bakery_List_Operator, GRT_UL_Action_Bakery_List, GRT_Action_Bakery_Property_Group, GRT_Action_Bakery_Global_Settings_Property_Group, GRT_PT_Action_Bakery]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.GRT_Action_Bakery = bpy.props.CollectionProperty(type=GRT_Action_Bakery_Property_Group)
    bpy.types.Scene.GRT_Action_Bakery_Index = bpy.props.IntProperty()

    bpy.types.Scene.GRT_Action_Bakery_Global_Settings = bpy.props.PointerProperty(type=GRT_Action_Bakery_Global_Settings_Property_Group)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.GRT_Action_Bakery
    del bpy.types.Scene.GRT_Action_Bakery_Index
    del bpy.types.Scene.GRT_Action_Bakery_Global_Settings

if __name__ == "__main__":
    register()
