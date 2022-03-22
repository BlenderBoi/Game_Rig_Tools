import bpy
import os
from . import Utility

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)

def draw_armature_visibility_options(self, context, layout):

    addon_preferences = context.preferences.addons[addon_name].preferences

    object = context.object

    if object:
        if object.type == "ARMATURE":
            if Utility.draw_subpanel(addon_preferences, addon_preferences.show_armature_display, "show_armature_display", "Armature Display", layout):


                layout.prop(object.data, "display_type", text="Display As")
                layout.prop(object.data, "show_names", text="Names")
                layout.prop(object.data, "show_bone_custom_shapes", text="Shapes")
                layout.prop(object.data, "show_group_colors", text="Group Colors")
                layout.prop(object, "show_in_front", text="In Front")

                row = layout.row(align=True)

                row.prop(object.data, "show_axes", text="Show Axes")
                row.prop(object.data, "axes_position", text="Position")




def draw_panel(self, context, layout):
    addon_preferences = context.preferences.addons[addon_name].preferences

    layout.label(text="Armature Constraint")

    row = layout.row(align=True)

    operator = row.operator("gamerigtool.toogle_constraint", text="Mute", icon="HIDE_ON")
    operator.mute = True
    operator.use_selected = addon_preferences.use_selected

    operator = row.operator("gamerigtool.toogle_constraint", text="Unmute", icon="HIDE_OFF")
    operator.mute = False
    operator.use_selected = addon_preferences.use_selected

    row.prop(addon_preferences, "use_selected", text="", icon="RESTRICT_SELECT_OFF")


    layout.label(text="Game Rig Tool")

    layout.operator("gamerigtool.generate_game_rig", text="Generate Game Rig")

    if Utility.draw_subpanel(addon_preferences, addon_preferences.show_utility, "show_utility", "Utility Tools", layout):

        layout.operator("gamerigtool.constraint_to_armature_name", text="Constraint to Armature Name", icon="CONSTRAINT_BONE")
        layout.operator("gamerigtool.batch_rename_actions", text="Batch Rename Actions", icon="SORTALPHA")
        layout.operator("gamerigtool.flatten_hierarchy", text="Flatten Hierarchy", icon="NOCURVE")
        layout.operator("gamerigtool.disconnect_all_bones", text="Disconnect All Bones", icon="GROUP_BONE")
        layout.operator("gamerigtool.apply_scale_op", text="Apply Armature Scale", icon="CON_SIZELIMIT")
        layout.operator("gamerigtool.convert_bendy_bones_to_bones", text="Convert Bendy Bones to Bones", icon="BONE_DATA")
        layout.operator("gamerigtool.unbind_mesh", text="Unbind Mesh", icon="ARMATURE_DATA")

        layout.operator("gamerigtool.batch_rename_vertex_groups", text="Batch Rename Vertex Groups", icon="GROUP_VERTEX")

        layout.operator("gamerigtool.bake_custom_properties", text="Bake Custom Properties", icon="PROPERTIES")

    if Utility.draw_subpanel(addon_preferences, addon_preferences.show_cleanup, "show_cleanup", "Clean Up Tools", layout):

        layout.operator("gamerigtool.unlock_bones_transform", text="Unlock Bones Transform", icon="UNLOCKED")
        layout.operator("gamerigtool.clear_all_bones_constraints", text="Clear All Bones Constraints", icon="CONSTRAINT")

        layout.operator("gamerigtool.remove_non_deform_bone", text="Remove Non Deform Bone", icon="BONE_DATA")
        layout.operator("gamerigtool.remove_animation_data", text="Remove Animation Data", icon="ACTION")
        layout.operator("gamerigtool.remove_bbone", text="Remove BBone", icon="BONE_DATA")
        layout.operator("gamerigtool.remove_bone_shape", text="Remove Bone Shapes", icon="CUBE")
        layout.operator("gamerigtool.remove_custom_property", text="Remove Custom Properties", icon="PROPERTIES")

        layout.operator("gamerigtool.move_all_bones_to_layer", text="Move All Bones to Layer", icon="SEQ_STRIP_DUPLICATE")



class CGD_PT_Deform_Rig_Side_Panel(bpy.types.Panel):

    bl_label = "GRT: Armature Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Game Rig Tools"

    def draw(self, context):
        layout = self.layout
        draw_panel(self, context, layout)
        draw_armature_visibility_options(self, context, layout)


classes = [CGD_PT_Deform_Rig_Side_Panel]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
