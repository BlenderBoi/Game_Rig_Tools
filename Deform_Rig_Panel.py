import bpy
import os

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


def draw_action_bakery(self, context, layout):
    addon_preferences = context.preferences.addons[addon_name].preferences

    scn = context.scene
    row = layout.row(align=True)
    row.alignment ="LEFT"

    if addon_preferences.show_action_bakery:
        row.prop(addon_preferences, "show_action_bakery", text="Action Bakery", emboss=False, icon="TRIA_DOWN")
        layout.template_list("CGD_UL_Action_Bakery_List", "", bpy.data, "actions", scn, "action_bakery_index")

        row = layout.row(align=True)
        row.operator("cgd.check_all_for_bake", text="Select All").mode = True
        row.operator("cgd.check_all_for_bake", text="Deselect All").mode = False

        if len(bpy.data.actions) > 0:
            active_action = bpy.data.actions[scn.action_bakery_index]

            # layout.prop(active_action, "use_custom_range", text="Use Custom Range")
            #
            # row = layout.row(align=True)
            #
            # if active_action.use_custom_range:
            #     row.prop(active_action, "custom_range_start", text="Custom Start")
            #     row.prop(active_action, "custom_range_end", text="Custom End")

            layout.prop(active_action, "loop", text="Loop")


            layout.label(text="Bake Objects")
            layout.prop(scn, "bake_control_armature", text="Control Armature")
            layout.prop(scn, "bake_deform_armature", text="Deform Armature")


            layout.prop(scn, "Push_to_NLA", text="Push to NLA")
            layout.prop(scn, "Unmute_Before_Bake", text="Unmute Constraint Before Bake")
            layout.prop(scn, "Mute_After_Bake", text="Mute Constraint After Bake")
            layout.operator("cgd.bake_action_bakery", text="Bake Action Bakery")

    else:
        row.prop(addon_preferences, "show_action_bakery", text="Action Bakery", emboss=False, icon="TRIA_RIGHT")

def draw_panel(self, context, layout):
    addon_preferences = context.preferences.addons[addon_name].preferences

    row = layout.row(align=True)

    operator = row.operator("gamerigtool.toogle_constraint", text="Mute")
    operator.mute = True
    operator.use_selected = addon_preferences.use_selected

    operator = row.operator("gamerigtool.toogle_constraint", text="Unmute")
    operator.mute = False
    operator.use_selected = addon_preferences.use_selected

    row.prop(addon_preferences, "use_selected", text="", icon="RESTRICT_SELECT_OFF")

    layout.operator("cgd.generate_game_rig", text="Generate Deform Rig")

    row = layout.row(align=True)
    row.alignment ="LEFT"

    if addon_preferences.show_tool:

        row.prop(addon_preferences, "show_tool", text="Semi Auto Toolkit", emboss=False, icon="TRIA_DOWN")

        # if context.mode == "OBJECT":
        #     layout.operator("cgd.constraint_to_armature_name", text="Constraint Armature by Bone Name")
        # if context.mode == "POSE":
        #     layout.operator("cgd.constraint_selected_bone_to_armature_name", text="Constraint Selected Bone to Armature By Name")
        #
        # layout.operator("cgd.remove_non_deform_bone", text="Remove Non Deform Bones")

        layout.operator("gamerigtool.constraint_to_armature_name", text="Constraint to Armature Name")
        layout.operator("gamerigtool.remove_non_deform_bone", text="Remove Non Deform Bone")

        layout.separator()
        col = layout.column(align=True)

        col.operator("gamerigtool.batch_rename_actions", text="Batch Rename Actions")
        col.operator("gamerigtool.remove_animation_data", text="Remove Animation Data and Drivers")
        col.operator("gamerigtool.remove_bbone", text="Remove BBone")
        col.operator("gamerigtool.remove_bone_shape", text="Remove Bone Shapes")
        col.operator("gamerigtool.remove_custom_property", text="Remove Custom Properties")





    else:
        row.prop(addon_preferences, "show_tool", text="Semi Auto Toolkit", emboss=False, icon="TRIA_RIGHT")

    draw_action_bakery(self, context, layout)


class CGD_PT_Deform_Rig_DATA_Panel(bpy.types.Panel):

    bl_label = "Game Rig Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):

        addon_preferences = context.preferences.addons[addon_name].preferences

        # if context.object:
        #     if context.object.type == "ARMATURE":


        if addon_preferences.armature_data:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout

        draw_panel(self, context, layout)

class CGD_PT_Deform_Rig_Side_Panel(bpy.types.Panel):

    bl_label = "Game Rig Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Game Rig Tools"

    @classmethod
    def poll(cls, context):

        addon_preferences = context.preferences.addons[addon_name].preferences
        #
        # if context.object:
        #     if context.object.type == "ARMATURE":


        if addon_preferences.side_panel:
            return True
        else:
            return False



    def draw(self, context):
        layout = self.layout
        draw_panel(self, context, layout)



classes = [CGD_PT_Deform_Rig_DATA_Panel, CGD_PT_Deform_Rig_Side_Panel]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
