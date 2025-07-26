import bpy
from .video_processing import AdvancedVideoReformatter, ReformatConfig

import asyncio
import bpy
from .video_processing import AdvancedVideoReformatter, ReformatConfig

class VIDEO_OT_process(bpy.types.Operator):
    """Process the video file"""
    bl_idname = "video.process"
    bl_label = "Process Video"

    def execute(self, context):
        try:
            scene = context.scene
            video_path = scene.social_uploader_video_path
            output_format = scene.social_uploader_output_format

            if not video_path:
                self.report({'ERROR'}, "Please select a video file")
                return {'CANCELLED'}

            self.report({'INFO'}, f"Processing video: {video_path}")

            reformatter = AdvancedVideoReformatter()
            config = self.get_reformat_config(reformatter, output_format)

            result = reformatter.reformat_video(video_path, config)

            self.report({'INFO'}, f"Video processing finished. Output files: {result}")

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

    def get_reformat_config(self, reformatter, output_format):
        if output_format == 'mp4':
            preset = reformatter.presets['web_optimized']
        elif output_format == 'webm':
            preset = reformatter.presets['webm']
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        return ReformatConfig(
            input_format=None,
            output_formats=[preset]
        )
