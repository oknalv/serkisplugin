bl_info = {
    "name": "Serkis Plugin",
    "author": "Eliot Blanco Lebrero",
    "category": "Animation",
    "location": "View 3D > Pose Mode > Animation"
}

import bpy
from .ui.gui import GenerateAnimationButton, InputFields, SerkisPanel


def register():
    bpy.utils.register_class(InputFields)
    bpy.types.Scene.fields = bpy.props.PointerProperty(type=InputFields)
    bpy.utils.register_class(GenerateAnimationButton)
    bpy.utils.register_class(SerkisPanel)


def unregister():
    del bpy.types.Scene.fields
    bpy.utils.unregister_class(GenerateAnimationButton)
    bpy.utils.unregister_class(SerkisPanel)
    bpy.utils.unregister_class(InputFields)


if __name__ == "__main__":
    register()
