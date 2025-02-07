import bpy

def transform_update_handler(scene):
    active_obj = bpy.context.active_object
    if active_obj:
        # Print a message whenever the transform is updated.
        print(f"Transform updated for: {active_obj.name}")

def register_handlers():
    if transform_update_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(transform_update_handler)

def unregister_handlers():
    if transform_update_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(transform_update_handler)
