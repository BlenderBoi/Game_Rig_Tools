
bl_info = {
    "name": "Game Rig Tools",
    "author": "BlenderBoi",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "description": "Generate a Deform Rig base on CGDive's Game-Ready Rig Video",
    "warning": "",
    "doc_url": "",
    "category": "Armature",
}

import bpy
from . import Deform_Rig_Generator
from . import Deform_Rig_Panel
from . import Preferences
from . import Action_Bakery

modules = [Deform_Rig_Generator, Deform_Rig_Panel, Preferences, Action_Bakery]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
