import bpy

from ..controller.controller import generate


class InputFields(bpy.types.PropertyGroup):
    InputFileName = bpy.props.StringProperty(name="", subtype="FILE_PATH", default="")
    FPS = bpy.props.FloatProperty(name="FPS", default=0.0, options={'HIDDEN'})
    ManualFPS = bpy.props.BoolProperty(name="Set FPS manually", default=False)


class SerkisPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "posemode"
    bl_category = "Serkis"
    bl_label = "Generate animation"


    def draw(self, context):
        layout = self.layout
        col1 = layout.column(align=True)
        col1.label("Input file:")
        col1.prop(context.scene.fields, "InputFileName")
        box1 = layout.box()
        box1.prop(context.scene.fields, "ManualFPS")
        row1 = box1.row()
        row1.prop(context.scene.fields, "FPS")
        col2 = layout.column(align=True)
        col2.operator("animation.generate_animation", text="Generate")


class GenerateAnimationButton(bpy.types.Operator):
    bl_idname = "animation.generate_animation"
    bl_label = "Generate"

    def invoke(self, context, event):
        fields = context.scene.fields
        if not fields.keys() or "InputFileName" not in fields.keys():
            raise TypeError("You must specify an input file")

        file = fields["InputFileName"]
        fps = None
        if "ManualFPS" in fields.keys() and fields["ManualFPS"] and "FPS" in fields.keys():
            fps = fields["FPS"]

        generate(file, fps)

        return {'FINISHED'}


