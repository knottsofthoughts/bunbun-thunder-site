# Copyright © 2023 Roblox Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# SPDX-License-Identifier: MIT

import sys
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the directory path of the current script
add_on_directory = Path(__file__).parent

# Append the dependencies directories to the path so we can access the bundled python modules
# If dependencies_public doesn't exist yet, the user is prompted to install them before using the plugin
dependencies_private = add_on_directory / "dependencies_private"
dependencies_public = add_on_directory / "dependencies_public"

for dep_path in (dependencies_private, dependencies_public):
    dep_str = str(dep_path)
    if dep_str not in sys.path:
        sys.path.append(dep_str)

MODULES_TO_RELOAD = (
    "event_loop",
    "status_indicators",
    "roblox_properties",
    "oauth2_login_operators",
    "RBX_OT_upload",
    "RbxOAuth2Client",
    "get_selected_objects",
    "constants",
    "creator_details",
    "RBX_OT_install_dependencies",
)


def reload_modules(module_names: tuple) -> None:
    """Safely reload specified modules with logging."""

    for name in module_names:
        module = globals().get(name)
        if module is None:
            continue

        try:
            importlib.reload(module)
            logger.debug("Successfully reloaded: %s", name)
        except Exception as e:  # pragma: no cover - best effort
            logger.warning("Failed to reload %s: %s", name, e, exc_info=True)


if "bpy" in locals():
    reload_modules(MODULES_TO_RELOAD)

try:
    import bpy
    from bpy.app.handlers import persistent
    from bpy.types import Panel, AddonPreferences
    from bpy.props import (
        StringProperty,
        PointerProperty,
        FloatProperty,
        IntProperty,
        BoolProperty,
    )
except ImportError as e:  # pragma: no cover - cannot happen outside Blender
    logger.error("Failed to import Blender modules: %s", e)
    raise

bl_info = {
    "name": "Upload to Roblox",
    "author": "Roblox",
    "description": "Uses Roblox's Open Cloud API to upload selected assets from Blender to Roblox",
    "blender": (3, 2, 0),
    "version": (0, 0, 0),  # Gets updated by Github Actions. See README for info
    "location": "View3D",
    "warning": "",
    "category": "Import-Export",
}


class RbxAddonPreferences(AddonPreferences):
    """AddOnPreferences that are serialized between Blender sessions"""

    bl_idname = __name__

    # These properties are not editable via preferences UI, they get reflected to and from properties in memory.
    # The only token we need to persist is the refresh token, since it gives all new tokens in the next session
    refresh_token: StringProperty()
    selected_creator_enum_index: IntProperty()

    # export_scale is configurable via the Add-on preferences menu in Blender
    from .lib import constants
