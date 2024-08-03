bl_info = {
    "name": "Physics to shapekeys/keyframes",
    "author": "WWhite",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "VIEW_3D > N",
    "description": "Based on Physics simulation creates multiple shapekeys and corresponding keyframes",
    "warning": "I'm new to this, so there may be bugs",
    "doc_url": "",
    "category": "",
}


import bpy
from bpy.types import (Panel,Operator)




def get_name():
    """Get the name for the currently active object"""
    return bpy.context.active_object.name




class MyProperties(bpy.types.PropertyGroup):
    

    #modifiers to choose from
    it=[('OP1',"Cloth",""),('OP2',"Soft body","")]

    my_enum:bpy.props.EnumProperty(name ="",description ="sample text",items=it)
    
    #First frame to save
    my_start:bpy.props.IntProperty(name="First frame", soft_min=0)
    
    #Last frame to save
    my_stop:bpy.props.IntProperty(name="Last frame", soft_min=0)
    
    #How often shape is saved
    my_step:bpy.props.IntProperty(name="Step", soft_min=1)



class MainOperation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "generate.1"
    bl_label = "gen"



    def execute(self, context):
        scene=context.scene
        mytool=scene.my_tool
        
        #properties to local var
        start=mytool.my_start
        stop=mytool.my_stop
        step=mytool.my_step

        mesh = bpy.context.object.data
        obj = bpy.context.object
        
        typ="" #type of selected modifier
        name="" #name of selected modifier
        
        
        if mytool.my_enum=='OP1':
            typ="CLOTH"
            
        if mytool.my_enum=='OP2':
            typ="SOFT_BODY"
        


        for modifier in obj.modifiers:

            #if selected modifier is in use, then we read its name
            if typ==modifier.type:
                name=modifier.name

            

        if start<stop and name!="":
            
            j=1
            #we go through all frames, last one included
            for i in range(start, stop+1,step):
                

                if stop+1<=i:
                    i=stop+1
                    step=1
                
                    


                #set current frame
                bpy.context.scene.frame_current = i
                
                #save modifier as shapekey
                bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=name)
                
                #help index and end help select shapekey
                index=j-start+1
                
                end=str(index-1)
                
                #select current shapekey
                bpy.context.object.active_shape_key_index = index

                
                
                #if shapekey dosent have end .00x
                if index==1:
                    #set current skapekey to 1 and inserts its keyframe
                    bpy.data.shape_keys["Key"].key_blocks[name].value = 1
                    bpy.context.object.data.shape_keys.key_blocks[name].keyframe_insert(data_path='value', frame=i)
                    
                    #set current skapekey to 0 and inserts its keyframe for next and previous frame
                    bpy.data.shape_keys["Key"].key_blocks[name].value = 0
                    bpy.context.object.data.shape_keys.key_blocks[name].keyframe_insert(data_path='value', frame=i+step)
                    bpy.context.object.data.shape_keys.key_blocks[name].keyframe_insert(data_path='value', frame=i-1)
                    
                else:
                    while len(end)<3:
                        temp="0"+end
                        end=temp
                    
                    #like above
                    bpy.data.shape_keys["Key"].key_blocks[name+"."+end].value = 1
                    bpy.context.object.data.shape_keys.key_blocks[name+"."+end].keyframe_insert(data_path='value', frame=i)
                    
                    bpy.data.shape_keys["Key"].key_blocks[name+"."+end].value = 0
                    bpy.context.object.data.shape_keys.key_blocks[name+"."+end].keyframe_insert(data_path='value', frame=i-step)
                    bpy.context.object.data.shape_keys.key_blocks[name+"."+end].keyframe_insert(data_path='value', frame=i+step)
                    
                j=j+1
                    
        return {'FINISHED'}
    

    
    
class CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Sim to skapekeys"
    bl_idname = "OBJECT_PT_StS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sim to skapekeys"

    def draw(self, context):
        
        layout = self.layout
        scene=context.scene
        mytool=scene.my_tool
        
        
        #select modifier
        layout.prop(mytool, "my_enum")
        
        #start and stop input
        layout.prop(mytool, "my_start")
        layout.prop(mytool, "my_stop")
        layout.prop(mytool, "my_step")

        
        #accept and run program
        row = layout.row()
        row.operator(MainOperation.bl_idname,text="Bake Skape Keys", icon='PLAY')


# Registration

from bpy.utils import register_class, unregister_class

_classes= [ MyProperties,MainOperation,CustomPanel]


def register():
    
    for cls in _classes:
        register_class(cls)

        bpy.types.Scene.my_tool=bpy.props.PointerProperty(type=MyProperties)
    


def unregister():
    for cls in _classes:
        unregister_class(cls)

        del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
