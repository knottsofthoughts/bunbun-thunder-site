import bpy

class SOCIAL_PT_video_processing(bpy.types.Panel):
    bl_label = "Video Processing"
    bl_idname = "SOCIAL_PT_video_processing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Social Uploader'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Select Video File:")
        layout.prop(scene, "social_uploader_video_path")

        layout.label(text="Output Format:")
        layout.prop(scene, "social_uploader_output_format")

def register():
    bpy.utils.register_class(SOCIAL_PT_video_processing)
    bpy.types.Scene.social_uploader_video_path = bpy.props.StringProperty(
        name="Video Path",
        description="Path to the video file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )
    bpy.types.Scene.social_uploader_output_format = bpy.props.EnumProperty(
        name="Output Format",
        description="Choose the output format for the video",
        items=[
            ('mp4', 'MP4', 'MPEG-4 video format'),
            ('webm', 'WebM', 'WebM video format'),
        ]
    )

def unregister():
    bpy.utils.unregister_class(SOCIAL_PT_video_processing)
    del bpy.types.Scene.social_uploader_video_path
    del bpy.types.Scene.social_uploader_output_format
