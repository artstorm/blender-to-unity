import bpy
import os
from pathlib import Path

class UT_Export(bpy.types.Operator):
    bl_idname = "unity.toolkit_export"
    bl_label = "Export"
    bl_description = "Export selected objects as fbx"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects
    
    def execute(self, context):
        try:
            self.export(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

    def export(self, context):
        # Find the root path to Unity.
        unity_root = self.get_root_path(context)

        # Make sure we're in object mode.
        bpy.ops.object.mode_set(mode='OBJECT')

        # Loop through the selected objects and export them one by one.
        selected_objects = context.selected_objects
        for obj in selected_objects:
            # Deselect all objects, and then reselect the object we are currently exporting.
            bpy.ops.object.select_all(action='DESELECT') 
            obj.select_set(state=True)

            # Check if the object has a custom path to append to the root.
            unity_path = bpy.data.objects[obj.name].get("unity_path", "")
            if unity_path:
                # We have a a custom path, create the directories to it, if not exist.
                path = Path(unity_root + unity_path)
                path.mkdir(parents=True, exist_ok=True)

            # Assemble the full path the file will be exported to.
            full_path = unity_root+unity_path+obj.name+".fbx"

            # Perform the export.
            bpy.ops.export_scene.fbx(
                filepath=full_path,
                path_mode='ABSOLUTE',
                check_existing=False,
                use_selection=True,
                object_types={'MESH'},
                bake_space_transform=True,
                mesh_smooth_type='OFF'
            )

            self.report({'INFO'}, obj.name + " exported to " + full_path)
    
        # Reselect the object to restore selection state before export.
        for obj in selected_objects:
            obj.select_set(True)

        # All done.
        self.report({'INFO'}, "Selected objects exported to " + unity_root)

    def get_root_path(self, context):
        """
        Get the absolute path to Unity where assets will be relatively exported.
        """
        # First try to see if we can find a file containing the absolute path. Using
        # a file for the path is the convenient way when multiple artists works
        # on the same project so each artist can use their own path.

        # Get the path to where the blend file is saved. Returns an empty string if the blend file has not been saved.
        blend_file_path = bpy.path.abspath("//")
        if blend_file_path:
            # Check if we have a unity.txt file where the blend file is saved.
            config_file = blend_file_path+"unity.txt"
            if os.path.exists(config_file):
                # Read the first line from the blend file, it should be the root path.
                with open(config_file) as f:
                    first_line = f.readline()
                    # Check so the expected path on the first line exists, if it does, we're done, return it.
                    if os.path.exists(first_line):
                        return first_line
                    else:
                        raise Exception("unity.txt file was found but did not contain a valid path.")

        # There was no unity.txt with a valid root path found.
        # Let's continue to see if we have an object that contains the root path.

        # Check if we have an object named unity
        if bpy.data.objects.get("unity"):
            # Get the unity_root attribute from the object if it exists
            root_path = bpy.data.objects["unity"].get("unity_root", None)
            if root_path:
                # Check so the root path exists.
                if os.path.exists(root_path):
                    return root_path
                else:
                    raise Exception("unity_root custom property was found but did not contain a valid path.")
            else:
                raise Exception("unity object was found but did not contain a unity_root custom property.")

        # We could not find a root path to Unity. Abort.
        raise Exception("Sorry, no valid root path to Unity found. Check the add-on doc of how to set it up.")
