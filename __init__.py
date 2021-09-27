
bl_info = {
    "name": "Game Rig Tools",
    "author": "BlenderBoi, Xin",
    "version": (1, 6, 0),
    "blender": (2, 80, 0),
    "description": "Generate a Deform Rig base on CGDive's Game-Ready Rig Video",
    "warning": "",
    "doc_url": "",
    "category": "Armature",
}

import bpy

from . import GRT_Extra_Operators

from . import Deform_Rig_Generator
from . import Deform_Rig_Panel
from . import Preferences

from . import GRT_Action_Bakery
from . import addition

modules = [addition, GRT_Extra_Operators, Deform_Rig_Generator, Deform_Rig_Panel, GRT_Action_Bakery, Preferences]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
