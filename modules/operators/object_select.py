import bpy
from bpy.props import *
from bpy.types import Operator


class OBJECT_OT_ml_select(Operator):
    bl_idname = "object.ml_select"
    bl_label = "Select Object"
    bl_description = ("Select object.\n"
                      "\n"
                      "Hold shift to extend selection")
    bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}

    object_name: StringProperty(options={'HIDDEN'}) # type: ignore
    unhide_object: BoolProperty(options={'HIDDEN', 'SKIP_SAVE'}) # type: ignore

    def execute(self, context):
        ob = bpy.data.objects[self.object_name]

        if not self.extend_selection:
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
    
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = ob

        if self.unhide_object:
            obj_collection = ob.users_collection[0]

            if obj_collection.hide_viewport == True or context.view_layer.layer_collection.children[obj_collection.name].hide_viewport == True:
                obj_collection.hide_viewport = False
                context.view_layer.layer_collection.children[obj_collection.name].hide_viewport = False
                for obj in obj_collection.objects:
                    obj.hide_set(True)
            ob.hide_set(False)
            
        ob.hide_viewport = False
        ob.select_set(True)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.extend_selection = True if event.shift else False

        return self.execute(context)
