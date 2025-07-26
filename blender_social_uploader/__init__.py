# SPDX-License-Identifier: MIT
import sys
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ADDON_DIR = Path(__file__).parent
for sub in ("dependencies_private", "dependencies_public"):
    dep = ADDON_DIR / sub
    if str(dep) not in sys.path:
        sys.path.append(str(dep))

MODULES_TO_RELOAD = (
    "audio_utils",
    "http_utils",
    "social_ot_upload",
    "ui",
    "video_ot_process",
    "video_processing",
)

def reload_modules(module_names):
    reloaded, failed = [], []
    for name in module_names:
        mod = globals().get(name)
        if not mod:
            continue
        try:
            importlib.reload(mod)
            reloaded.append(name)
            logger.debug(f"Reloaded module: {name}")
        except Exception as e:
            failed.append(name)
            logger.warning(f"Failed to reload {name}: {e}", exc_info=True)

    if reloaded:
        logger.info(f"[reload] succeeded for: {', '.join(reloaded)}")
    if failed:
        logger.error(f"[reload] FAILED for: {', '.join(failed)}")

if "bpy" in locals():
    reload_modules(MODULES_TO_RELOAD)

try:
    import bpy
    from bpy.types import Panel, AddonPreferences
    from bpy.props import StringProperty, PointerProperty, FloatProperty, IntProperty, BoolProperty
except ImportError as e:
    logger.error(f"Blender import failure: {e}")
    raise

bl_info = {
    "name": "Blender Social Uploader",
    "author": "Jules",
    "description": "Upload assets from Blender to various social media platforms.",
    "blender": (3, 2, 0),
    "version": (0, 1, 0),
    "location": "View3D",
    "warning": "",
    "category": "Import-Export",
}

from .lib.social_ot_upload import SOCIAL_OT_upload
from .lib.video_ot_process import VIDEO_OT_process
from .lib import ui

classes = (
    SOCIAL_OT_upload,
    ui.SOCIAL_PT_video_processing,
    VIDEO_OT_process,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    ui.register()
    logger.info("blender-social-uploader registered")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    ui.unregister()
    logger.info("blender-social-uploader unregistered")
