import bpy
from bpy.types import Panel
import requests

# Define the server base URL
SERVER_BASE_URL = "http://127.0.0.1:5000"

# List to collect panel classes for registration.
panel_classes = []
bpy.types.Scene.inventory_loaded = bpy.props.BoolProperty(default=False)
class OBJECT_PT_TransformControls(Panel):
    bl_label = "Transform Controls"
    bl_idname = "VIEW3D_PT_transform_controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj:
            col = layout.column(align=True)
            col.label(text="Position:")
            col.prop(obj, "location", text="")
            col.label(text="Rotation:")
            col.prop(obj, "rotation_euler", text="")
            col.label(text="Scale:")
            col.prop(obj, "scale", text="")
        else:
            layout.label(text="No active object selected.")


class OBJECT_PT_EndpointSelector(Panel):
    bl_label = "Endpoint Selection"
    bl_idname = "VIEW3D_PT_endpoint_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "endpoint_options", text="Endpoint")

class OBJECT_PT_SubmitPanel(Panel):
    bl_label = "Submit Transform Data"
    bl_idname = "VIEW3D_PT_submit_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.submit_transform", text="Submit Transform Data")
        layout.operator("object.get_file_path", text="Get File Path")

class VIEW3D_PT_ShowInventoryPanel(bpy.types.Panel):
    bl_label = "Show Inventory"
    bl_idname = "VIEW3D_PT_show_inventory"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.show_inventory", text="Show Inventory")

        if getattr(context.scene, "show_inventory", False):
            try:
                response = requests.get(f"{SERVER_BASE_URL}/inventory", timeout=20)
                if response.status_code == 200:
                    inventory_items = response.json()
                    
                    # Create UI elements without modifying scene properties
                    box = layout.box()
                    row = box.row()
                    row.label(text="Item Name")
                    row.label(text="Quantity")

                    # Display inventory items
                    for item in inventory_items:
                        row = box.row()
                        row.label(text=str(item['name']))
                        row.label(text=str(item['quantity']))
                else:
                    layout.label(text="Failed to fetch inventory")
            except Exception as e:
                layout.label(text=f"Error connecting to server: {str(e)}")


class OBJECT_PT_DatabaseManager(Panel):
    bl_label = "Inventory Manager"
    bl_idname = "VIEW3D_PT_database_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Item management UI
        box = layout.box()
        box.label(text="Item Management:")
        box.prop(scene, "item_name", text="Name")
        box.prop(scene, "item_quantity", text="Quantity")
        
        row = box.row()
        row.operator("object.add_item")
        row.operator("object.remove_item")
        row.operator("object.update_item")


    
class OBJECT_PT_ObjectSelector(Panel):
    bl_label = "Object Selector"
    bl_idname = "VIEW3D_PT_object_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Transform Manager"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Add object search/selection field
        layout.prop_search(
            scene, "selected_object", 
            scene, "objects",
            text="Object"
        )
        
        # Show active object info
        active_obj = context.active_object
        if active_obj:
            layout.label(text=f"Active: {active_obj.name}")
# In panels.py, add this line with other panel registrations
panel_classes.append(OBJECT_PT_TransformControls)
panel_classes.append(OBJECT_PT_EndpointSelector)
panel_classes.append(OBJECT_PT_SubmitPanel)
panel_classes.append(VIEW3D_PT_ShowInventoryPanel)
panel_classes.append(OBJECT_PT_DatabaseManager)
panel_classes.append(OBJECT_PT_ObjectSelector)

