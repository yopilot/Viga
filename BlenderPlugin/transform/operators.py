import bpy
import requests
import os
from .websocket_manager import ws_manager
from bpy.types import Operator

# List to collect operator classes for registration.
operator_classes = []


# Change the URL to match your server configuration.
SERVER_BASE_URL = "http://127.0.0.1:5000"

bpy.types.Scene.show_inventory = bpy.props.BoolProperty(
    name="Show Inventory",
    default=False
)

class OBJECT_OT_ToggleInventory(bpy.types.Operator):
    bl_idname = "object.toggle_inventory"
    bl_label = "Toggle Inventory"
    
    def execute(self, context):
        context.scene.show_inventory = not context.scene.show_inventory
        return {'FINISHED'}

class OBJECT_OT_ShowInventory(Operator):
    bl_idname = "object.show_inventory"
    bl_label = "Show Inventory"
    
    def execute(self, context):
        context.scene.show_inventory = not context.scene.show_inventory
        
        # Use a separate operator call to update the inventory_loaded state
        if context.scene.show_inventory:
            bpy.ops.object.refresh_inventory()
        return {'FINISHED'}

class OBJECT_OT_RefreshInventory(Operator):
    bl_idname = "object.refresh_inventory"
    bl_label = "Refresh Inventory"
    
    def execute(self, context):
        context.scene.inventory_loaded = False
        return {'FINISHED'}


class OBJECT_OT_GetFilePath(Operator):
    bl_idname = "object.get_file_path"
    bl_label = "Get File Path"
    
    def execute(self, context):
        active_obj = context.active_object
        endpoint_option = context.scene.endpoint_options
        
        if not active_obj:
            self.report({'WARNING'}, "No active object selected!")
            return {'CANCELLED'}
        
        # Collect transform data with consistent naming
        transform_data = {
            "name": active_obj.name,
            "position": list(active_obj.location),
            "rotation": list(active_obj.rotation_euler),
            "scale": list(active_obj.scale)
        }
        
        # Create endpoint-specific payloads
        if endpoint_option == 'transform':
            payload = transform_data
        elif endpoint_option == 'translation':
            payload = {
                "name": active_obj.name,
                "position": transform_data["position"]  # matches TranslationData model
            }
        elif endpoint_option == 'rotation':
            payload = {
                "name": active_obj.name,
                "rotation": transform_data["rotation"]
            }
        elif endpoint_option == 'scale':
            payload = {
                "name": active_obj.name,
                "scale": transform_data["scale"]
            }
        else:
            self.report({'ERROR'}, "Unknown endpoint option!")
            return {'CANCELLED'}
        
        url = f"{SERVER_BASE_URL}/{endpoint_option}"
        
        try:
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                self.report({'INFO'}, f"Data sent successfully to {url}")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, f"Server error {response.status_code}: {response.text}")
                return {'CANCELLED'}
        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"Failed to send request: {e}")
            return {'CANCELLED'}

 

            

class OBJECT_OT_AddItem(Operator):
    bl_idname = "object.add_item"
    bl_label = "Add Item"
    
    def execute(self, context):
        if not context.scene.item_name:
            self.report({'ERROR'}, "Item name cannot be empty")
            return {'CANCELLED'}
            
        if context.scene.item_quantity < 0:
            self.report({'ERROR'}, "Quantity cannot be negative")
            return {'CANCELLED'}
            
        data = {
            "name": context.scene.item_name,
            "quantity": context.scene.item_quantity
        }
        
        try:
            response = requests.post(
                f"{SERVER_BASE_URL}/add-item",
                json=data,
                timeout=20
            )
            if response.status_code == 200:
                self.report({'INFO'}, response.json().get("message", "Item added successfully"))
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Server error: {response.status_code}")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error adding item: {str(e)}")
            return {'CANCELLED'}

class OBJECT_OT_RemoveItem(Operator):
    bl_idname = "object.remove_item"
    bl_label = "Remove Item"
    
    def execute(self, context):
        try:
            # Get the item name from the scene properties
            item_name = context.scene.item_name
            
            if not item_name:
                self.report({'ERROR'}, "Please enter an item name")
                return {'CANCELLED'}
                
            # Send only the name to the server
            data = {"name": item_name}
            
            response = requests.post(
                f"{SERVER_BASE_URL}/remove-item",
                json=data,
                timeout=20
            )
            
            if response.status_code == 200:
                self.report({'INFO'}, f"Item {item_name} removed successfully")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Server error: {response.status_code}")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

    
class OBJECT_OT_UpdateItem(Operator):
    bl_idname = "object.update_item"
    bl_label = "Update Item"
    
    def execute(self, context):
        try:
            # Get the item details from the scene properties
            item_name = context.scene.item_name
            quantity = context.scene.item_quantity
            
            if not item_name:
                self.report({'ERROR'}, "Please enter an item name")
                return {'CANCELLED'}
                
            data = {
                "name": item_name,
                "quantity": quantity
            }
            
            # Change from /update-item to /update-quantity
            response = requests.post(
                f"{SERVER_BASE_URL}/update-quantity",  # Changed URL
                json=data,
                timeout=20
            )
            
            if response.status_code == 200:
                self.report({'INFO'}, f"Item {item_name} updated successfully")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Server error: {response.status_code}")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        

class OBJECT_OT_GetFilePath(Operator):
    bl_idname = "object.get_file_path"
    bl_label = "Get File Path"
    
    def execute(self, context):
        try:
            # Get actual Blender file path
            blend_file_path = bpy.data.filepath
            project_path = os.path.dirname(blend_file_path)
            
            data = {
                "file_path": blend_file_path,
                "project_path": project_path
            }
            
            response = requests.post(
                f"{SERVER_BASE_URL}/file-path",
                json=data,
                timeout=20
            )
            if response.status_code == 200:
                self.report({'INFO'}, f"File Path: {blend_file_path}")
            
        except Exception as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}


class OBJECT_OT_SubmitTransform(Operator):
    bl_idname = "object.submit_transform"
    bl_label = "Submit Transform Data"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_obj = context.active_object
        endpoint_option = context.scene.endpoint_options
        
        if not active_obj:
            self.report({'WARNING'}, "No active object selected!")
            return {'CANCELLED'}
        
        # Collect transform data from the active object.
        transform_data = {
            "name": active_obj.name,
            "position": list(active_obj.location),
            "rotation": list(active_obj.rotation_euler),
            "scale": list(active_obj.scale)
        }
        
        # Choose the payload based on the selected endpoint.
        if endpoint_option == 'transform':
            payload = transform_data
        elif endpoint_option == 'translation':
            payload = {"name": active_obj.name, "position": transform_data["position"]}
        elif endpoint_option == 'rotation':
            payload = {"name": active_obj.name, "rotation": transform_data["rotation"]}
        elif endpoint_option == 'scale':
            payload = {"name": active_obj.name, "scale": transform_data["scale"]}
        else:
            self.report({'ERROR'}, "Unknown endpoint option!")
            return {'CANCELLED'}
        
        url = f"{SERVER_BASE_URL}/{endpoint_option}"
        
        try:
            # The request timeout is set to 20 seconds.
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                self.report({'INFO'}, f"Data sent successfully to {url}")
            else:
                self.report({'WARNING'}, f"Server error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"Failed to send request: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
operator_classes.append(OBJECT_OT_ToggleInventory)
operator_classes.append(OBJECT_OT_SubmitTransform)
operator_classes.append(OBJECT_OT_AddItem)
operator_classes.append(OBJECT_OT_RemoveItem)
operator_classes.append(OBJECT_OT_UpdateItem)
operator_classes.append(OBJECT_OT_GetFilePath)
operator_classes.append(OBJECT_OT_ShowInventory)
operator_classes.append(OBJECT_OT_RefreshInventory)