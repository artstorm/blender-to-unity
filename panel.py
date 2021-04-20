import bpy

class UT_Panel(bpy.types.Panel):
    bl_idname = "UNITY_TOOLKIT_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Unity Export Toolkit"
    bl_category = "Unity"
    
    def draw(self, context):        
        layout = self.layout

        row = layout.row()
        row.operator('unity.toolkit_export', text='Export')
