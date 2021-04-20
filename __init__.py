bl_info = {
    "name" : "Unity Export Toolkit",
    "author" : "Johan Steen, @artstorm",
    "description" : "Provides functionality for a streamlined export workflow to Unity.",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "Unity Panel",
    "warning" : "",
    "wiki_url": "https://github.com/artstorm/blender-to-unity",
    "category" : "Import-Export"
}

import bpy
from . panel import UT_Panel
from . operators.export import UT_Export

classes = ( 
    UT_Panel, 
    UT_Export 
)

def register():
    for cls in classes:
       bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
