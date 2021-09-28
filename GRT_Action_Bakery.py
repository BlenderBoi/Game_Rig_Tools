import bpy
from . import Utility
import os
from bpy_extras import anim_utils


script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


class GRT_Load_Action_Menu(bpy.types.Menu):
    bl_label = "Load Action Menu"
    bl_idname = "GRT_MT_load_action_menu"

    def draw(self, context):
        layout = self.layout

        Operator = layout.operator("gamerigtool.action_bakery_list_operator", text="Load Action By Name", icon="SORTALPHA")
        Operator.operation = "LOAD_ACTION_BY_NAME"

        Operator = layout.operator("gamerigtool.action_bakery_list_operator", text="Load All Action", icon="IMPORT")
        Operator.operation = "LOAD_ALL_ACTIONS"

        Operator = layout.operator("gamerigtool.action_bakery_list_operator", text="Load From NLA", icon="NLA_PUSHDOWN")
        Operator.operation = "LOAD_FROM_NLA"

        Operator = layout.operator("gamerigtool.batch_rename_actions", text="Batch Rename Actions", icon="SORTALPHA")

class GRT_Action_Bakery_Set_Frame_Range_To_Action(bpy.types.Operator):
    """Set Frame Range to Action"""
    bl_idname = "gamerigtool.action_bakery_set_frame_range_to_action"
    bl_label = "Set Frame Range To Action"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()

    def execute(self, context):

        scn = context.scene
        item_list = scn.GRT_Action_Bakery
        item_index = self.index

        active_baker = item_list[item_index]

        if active_baker.Action:
            active_baker.Set_FR_Start = active_baker.Action.frame_range[0]
            active_baker.Set_FR_End = active_baker.Action.frame_range[1]


        Utility.update_UI()

        return {'FINISHED'}

ENUM_list_operation = [("ADD","Add","Add"),("REMOVE","Remove","Remove"),("UP","Up","Up"), ("DOWN","Down","Down"),("ASSIGN","Assign","Assign"),("UNASSIGN","Unassign","Unassign"), ("LOAD_ALL_ACTIONS", "Load All Actions", "Load All Actions"), ("LOAD_ACTIVE_ACTIONS", "Load Active Actions", "Load Active Actions"), ("LOAD_ACTION_BY_NAME", "Load Action By Name", "Load Action By Name"), ("LOAD_FROM_NLA", "Load From NLA", "Load From NLA"), ("CLEAR_ALL_ACTIONS", "Clear All Action", "Clear All Action")]

class GRT_Action_Bakery_List_Operator(bpy.types.Operator):
    """List Operator"""
    bl_idname = "gamerigtool.action_bakery_list_operator"
    bl_label = "List Operator"
    bl_options = {'UNDO', 'REGISTER'}

    operation: bpy.props.EnumProperty(items=ENUM_list_operation)
    action: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    assign: bpy.props.BoolProperty(default=True)
    name_include: bpy.props.StringProperty()

    def draw(self, context):
        if self.operation == "ADD":
            layout = self.layout
            layout.prop_search(self, "action", bpy.data, "actions" ,text="Action")
        if self.operation == "LOAD_ACTION_BY_NAME":
            layout = self.layout
            layout.prop(self, "name_include", text="Name Include")

    def invoke(self, context, event):

        if self.operation in ["ADD", "LOAD_ACTION_BY_NAME"]:
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

        if self.operation == "CLEAR_ALL_ACTIONS":


            item_list.clear()

            return {'FINISHED'}


        if self.operation == "LOAD_FROM_NLA":

            object = context.object
            if object:
                if object.type == "ARMATURE":


                    if object.animation_data:

                        for nla_track in object.animation_data.nla_tracks:

                            for nla_strip in nla_track.strips:



                                action = nla_strip.action

                                if action:

                                    check = [item.Action for item in item_list]

                                    if not action in check:
                                        item = item_list.add()
                                        item.Action = action
                                        item.LOCAL_Baked_Name = "BAKED_" + action.name

                                        item.Set_FR_Start = action.frame_range[0]
                                        item.Set_FR_End = action.frame_range[1]

                                        scn.GRT_Action_Bakery_Index = len(item_list) - 1


            Utility.update_UI()

            return {'FINISHED'}



        if self.operation == "LOAD_ACTION_BY_NAME":

            for action in bpy.data.actions:

                check = [item.Action for item in item_list]

                if not action in check:
                    if self.name_include in action.name:
                        item = item_list.add()
                        item.Action = action
                        item.LOCAL_Baked_Name = "BAKED_" + action.name

                        item.Set_FR_Start = action.frame_range[0]
                        item.Set_FR_End = action.frame_range[1]

                        scn.GRT_Action_Bakery_Index = len(item_list) - 1

            Utility.update_UI()

            return {'FINISHED'}




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
                            item.LOCAL_Baked_Name = "BAKED_" + action.name

                            item.Set_FR_Start = action.frame_range[0]
                            item.Set_FR_End = action.frame_range[1]

                            scn.GRT_Action_Bakery_Index = len(item_list) - 1

            Utility.update_UI()

            return {'FINISHED'}


        if self.operation == "LOAD_ALL_ACTIONS":

            for action in bpy.data.actions:

                check = [item.Action for item in item_list]

                if not action in check:
                    item = item_list.add()
                    item.Action = action
                    item.LOCAL_Baked_Name = "BAKED_" + action.name

                    item.Set_FR_Start = action.frame_range[0]
                    item.Set_FR_End = action.frame_range[1]

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
                item.Action = Action

                item.LOCAL_Baked_Name = "BAKED_" + Action.name


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


        # row = row.row(align=True)
        # row.alignment = "RIGHT"
        # row.prop(item, "use_loop", text="", icon="FILE_REFRESH")

        Operator = row.operator("gamerigtool.action_bakery_list_operator", text="", icon="X")
        Operator.operation = "REMOVE"
        Operator.index = index


            # row.prop(Action, "name", text="")

class GRT_PT_Action_Bakery(bpy.types.Panel):

    bl_label = "Action Bakery"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Game Rig Tools"

    # @classmethod
    # def poll(cls, context):

        #Top Bar Toogle Constraint Update

        # addon_preferences = context.preferences.addons[addon_name].preferences
        #
        # if addon_preferences.side_panel:
        #     return True
        # else:
        #     return False

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

        col.separator()
        col.menu("GRT_MT_load_action_menu", text="", icon="DOWNARROW_HLT")
        col.separator()

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="TRIA_UP")
        Operator.operation = "UP"
        Operator.index = scn.GRT_Action_Bakery_Index

        Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="TRIA_DOWN")
        Operator.operation = "DOWN"
        Operator.index = scn.GRT_Action_Bakery_Index



        # Operator = col.operator("gamerigtool.action_bakery_list_operator", text="", icon="SORTALPHA")
        # Operator.operation = "LOAD_ACTION_BY_NAME"
        #
        #
        #

        # Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="All Action", icon="IMPORT")
        # Operator.operation = "LOAD_ALL_ACTIONS"
        LOAD_ACTION_ENABLE =False

        object = context.object
        if object:
            if object.type == "ARMATURE":
                if object.animation_data:
                    if object.animation_data.action:
                        LOAD_ACTION_ENABLE = True




        row2 = col2.row(align=True)
        row2.enabled = LOAD_ACTION_ENABLE
        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="Active", icon="IMPORT")
        Operator.operation = "LOAD_ACTIVE_ACTIONS"

        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="From NLA", icon="NLA_PUSHDOWN")
        Operator.operation = "LOAD_FROM_NLA"

        row2 = col2.row(align=True)

        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="Load All", icon="IMPORT")
        Operator.operation = "LOAD_ALL_ACTIONS"

        Operator = row2.operator("gamerigtool.action_bakery_list_operator", text="Clear All", icon="TRASH")
        Operator.operation = "CLEAR_ALL_ACTIONS"


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

                # if Utility.draw_subpanel(active_baker, active_baker.SHOW_Local_Settings, "SHOW_Local_Settings", "Local Settings", layout):

                layout.label(text="Local Settings")

                col3 = layout.column(align=True)
                col3.prop(active_baker, "use_Local_Name", text="Set Baked Action name")

                if active_baker.use_Local_Name:
                    col3.prop(active_baker, "LOCAL_Baked_Name", text="")

                # row3 = col3.row(align=True)
                # row3.prop(active_baker, "use_loop", text="Loop", icon="FILE_REFRESH")

                #
                # if not active_baker.use_loop:
                #

                if active_baker.Action:
                    col3.separator()
                    col3.label(text="Frame Range")
                    row3 = col3.row(align=True)
                    row3.prop(active_baker, "Frame_Range_Mode", expand=True)

                    if active_baker.Frame_Range_Mode == "ACTION":
                        row3 = col3.row(align=True)
                        # row3.prop(active_baker.Action, "frame_range", text="")
                        row3.label(text="Start: " + str(active_baker.Action.frame_range[0]), icon="ACTION")
                        row3.label(text="End: " + str(active_baker.Action.frame_range[1]), icon="ACTION")
                        col3.separator()

                    if active_baker.Frame_Range_Mode == "SET":
                        row3 = col3.row(align=True)
                        row3.prop(active_baker, "Set_FR_Start", text="Set Start")
                        row3.prop(active_baker, "Set_FR_End", text="Set End")
                        row3.operator("gamerigtool.action_bakery_set_frame_range_to_action", text="", icon="FILE_REFRESH").index = scn.GRT_Action_Bakery_Index
                        col3.separator()

                    if active_baker.Frame_Range_Mode == "TRIM":
                        row3 = col3.row(align=True)
                        row3.prop(active_baker, "Trim_FR_Start", text="Trim Start")
                        row3.prop(active_baker, "Trim_FR_End", text="Trim End")

                        row3 = col3.row(align=True)
                        row3.label(text="Start: " + str(active_baker.Action.frame_range[0] + active_baker.Trim_FR_Start), icon="SCULPTMODE_HLT")
                        row3.label(text="End: "+ str(active_baker.Action.frame_range[1] - active_baker.Trim_FR_End), icon="SCULPTMODE_HLT")
                        col3.separator()

                    col3.prop(active_baker, "offset_keyframe_to_frame_one", text="Offset to Frame One")
                # if active_baker.use_Local_Trim:
                #
                #     col3.prop(active_baker, "LOCAL_Trim", text="Trim")




                layout.separator()






        layout.label(text="Bake Settings")


        col = layout.column(align=True)
        col.label(text="Control Rig")
        col.prop(Global_Settings, "Source_Armature", text="")
        col.label(text="Game Rig")
        col.prop(Global_Settings, "Target_Armature", text="")

        layout.separator()


        if not Global_Settings.Source_Armature:
            layout.label(text="Select Control Rig", icon="ERROR")
        if not Global_Settings.Target_Armature:
            layout.label(text="Select Game Rig", icon="ERROR")



        row = layout.row(align=True)
        row.operator("gamerigtool.bake_action_bakery")
        row.prop(Global_Settings, "Bake_Popup", text="", icon="SETTINGS")

        layout.prop(Global_Settings, "Overwrite", text="Overwrite")

        layout.prop(Global_Settings, "Push_to_NLA", text="Push To NLA")

        layout.separator()







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

    # layout.separator()
    #
    # layout.label(text="Trim End")
    # row = layout.row(align=True)
    # row.prop(Global_Settings, "GLOBAL_Trim_End_Frame", text="")

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

def UPDATE_SET_Start(self, context):
    if self.Set_FR_Start >= self.Set_FR_End:
        self.Set_FR_End = self.Set_FR_Start + 1

def UPDATE_SET_End(self, context):
    if self.Set_FR_End <= self.Set_FR_Start:
        self.Set_FR_Start = self.Set_FR_End - 1

#Set to Action

def UPDATE_TRIM_Start(self, context):
    if self.Action:
        start = self.Action.frame_range[0] + self.Trim_FR_Start
        end = self.Action.frame_range[1] - self.Trim_FR_End

        if start >= end:


            self.Trim_FR_Start = end-2

def UPDATE_TRIM_End(self, context):

    if self.Action:
        start = self.Action.frame_range[0] + self.Trim_FR_Start
        end = self.Action.frame_range[1] - self.Trim_FR_End

        if end <= start:

            self.Trim_FR_End = self.Action.frame_range[1] - self.Action.frame_range[0] + self.Trim_FR_Start -1


ENUM_Trim_Type = [("KEYFRAME","Keyframe","Keyframe"),("NLA_STRIP","NLA Strip","NLA Strip")]
ENUM_Frame_Range_Mode = [("ACTION","Action","Action"),("SET","Set","Set"),("TRIM","Trim","Trim")]
class GRT_Action_Bakery_Property_Group(bpy.types.PropertyGroup):

    Action : bpy.props.PointerProperty(name="Action", type=bpy.types.Action)
    Bake_Select: bpy.props.BoolProperty(default=True)


    SHOW_Local_Settings: bpy.props.BoolProperty(default=False)

    use_Local_Name: bpy.props.BoolProperty()
    LOCAL_Baked_Name: bpy.props.StringProperty()

    use_Local_Trim: bpy.props.BoolProperty()

    Frame_Range_Mode: bpy.props.EnumProperty(items=ENUM_Frame_Range_Mode)
    Set_FR_Start: bpy.props.IntProperty(min=0, update=UPDATE_SET_Start)
    Set_FR_End: bpy.props.IntProperty(min=1, default=1, update=UPDATE_SET_End)

    Trim_FR_Start: bpy.props.IntProperty(min=0, update=UPDATE_TRIM_Start)
    Trim_FR_End: bpy.props.IntProperty(min=0, update=UPDATE_TRIM_End)

    offset_keyframe_to_frame_one: bpy.props.BoolProperty(default=False)

    # use_loop: bpy.props.BoolProperty()
    LOCAL_Trim: bpy.props.IntProperty(min=0)

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

        CTRL_Save_Use_ACTION = None

        if control_rig.animation_data:

            CTRL_Save_Use_NLA = control_rig.animation_data.use_nla
            control_rig.animation_data.use_nla = False
            CTRL_Save_Use_ACTION = control_rig.animation_data.action

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



                                    # else:
                                    #     frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1])+1-Global_Settings.GLOBAL_Trim_End_Frame)]

                                if Baker.Frame_Range_Mode == "SET":
                                    start_frame = Baker.Set_FR_Start
                                    end_frame = Baker.Set_FR_End + 1
                                if Baker.Frame_Range_Mode == "ACTION":
                                    start_frame = int(action.frame_range[0])
                                    end_frame = int(action.frame_range[1]) + 1
                                if Baker.Frame_Range_Mode == "TRIM":
                                    start_frame = int(action.frame_range[0]) + Baker.Trim_FR_Start
                                    end_frame = int(action.frame_range[1]) + 1 - Baker.Trim_FR_End


                                frame = [i for i in range(start_frame, end_frame)]



                                # if Baker.use_Local_Trim:
                                #     frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1])+1-Baker.LOCAL_Trim)]
                                # else:
                                #     frame = [i for i in range(int(action.frame_range[0]), int(action.frame_range[1])+1)]


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



                                if Baker.offset_keyframe_to_frame_one:

                                    start_frame = Baked_Action[0].frame_range[0]

                                    for fcurve in Baked_Action[0].fcurves:
                                        for kp in fcurve.keyframe_points:
                                            kp.co.x = kp.co.x - start_frame + 1

                                context.view_layer.update()


                                if Global_Settings.Push_to_NLA:
                                    deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, Baked_Action[0].frame_range[0], Baked_Action[0])
                                    # deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, action.frame_range[0], Baked_Action[0])
                                    # deform_rig.animation_data.nla_tracks.new().strips.new(Baked_Action[0].name, 0, Baked_Action[0])


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
                                control_rig.animation_data.action = CTRL_Save_Use_ACTION

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





























classes = [GRT_Action_Bakery_Set_Frame_Range_To_Action, GRT_Load_Action_Menu, GRT_Bake_Action_Bakery, GRT_Action_Bakery_List_Operator, GRT_UL_Action_Bakery_List, GRT_Action_Bakery_Property_Group, GRT_Action_Bakery_Global_Settings_Property_Group, GRT_PT_Action_Bakery]


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
