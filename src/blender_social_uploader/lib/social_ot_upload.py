import os
import bpy
from bpy.props import StringProperty
from blender_social_uploader.lib.audio_utils import convert_wma_to_wav
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

    def execute(self, context):
        filepath = self.filepath
        ext = os.path.splitext(filepath)[1].lower().lstrip(".")

        if ext == "wma":
            self.report({'INFO'}, "🛠️ Converting WMA to WAV…")
            try:
                filepath = convert_wma_to_wav(filepath)
            except Exception as e:
                self.report({'ERROR'}, f"Audio conversion failed: {e}")
                return {'CANCELLED'}

        # TODO: Add platform selection logic here
        self.report({'INFO'}, f"File selected: {os.path.basename(filepath)}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
