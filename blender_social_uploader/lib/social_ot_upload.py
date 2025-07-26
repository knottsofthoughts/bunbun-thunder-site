import os
import bpy
import asyncio
from bpy.props import StringProperty
from .audio_utils import convert_wma_to_wav
from .http_utils import upload_file
from .video_processing import AdvancedVideoReformatter, ReformatConfig

class SOCIAL_OT_upload(bpy.types.Operator):
    """Upload selected asset to a social media platform"""
    bl_idname = "social.upload_asset"
    bl_label = "Upload to Social Media"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.png;*.fbx;*.obj;*.wav;*.mp3;*.wma",
        options={'HIDDEN'},
        description="Choose an asset or sound file to upload"
    )
    filepath: StringProperty(subtype="FILE_PATH")
    title: StringProperty(name="Title", description="Title for the upload")
    description: StringProperty(name="Description", description="Description for the upload")

    def execute(self, context):
        try:
            filepath = self.filepath
            ext = os.path.splitext(filepath)[1].lower().lstrip(".")

            video_extensions = ["mp4", "mov", "avi", "mkv", "webm"]

            if ext in video_extensions:
                self.report({'INFO'}, "Processing video...")
                reformatter = AdvancedVideoReformatter()
                preset = reformatter.presets['web_optimized']
                config = ReformatConfig(input_format=None, output_formats=[preset])
                processed_files = reformatter.reformat_video(filepath, config)
                if not processed_files:
                    raise Exception("Video processing failed to produce any files.")
                filepath = processed_files[0]
                self.report({'INFO'}, "Video processing complete.")

            elif ext == "wma":
                self.report({'INFO'}, "🛠️ Converting WMA to WAV…")
                filepath = convert_wma_to_wav(filepath)
                self.report({'INFO'}, "Audio conversion complete.")

            self.report({'INFO'}, "Uploading file...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(upload_file(filepath, self.title, self.description))
            self.report({'INFO'}, "Upload complete.")

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "title")
        layout.prop(self, "description")
