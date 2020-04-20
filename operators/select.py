import bpy
from bpy.props import EnumProperty
from mathutils import Vector


axis_items = [("0", "X", ""),
              ("1", "Y", ""),
              ("2", "Z", "")]


class SelectCenterObjects(bpy.types.Operator):
    bl_idname = "machin3.select_center_objects"
    bl_label = "MACHIN3: 选择中心对象"
    bl_description = "选择位于中心的对象,对象,在X，Y或Z轴的两侧都具有顶点."
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(name="轴向", items=axis_items, default="0")

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.row()
        row.prop(self, "axis", expand=True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        visible = [obj for obj in context.visible_objects if obj.type == "MESH"]

        if visible:

            bpy.ops.object.select_all(action='DESELECT')

            for obj in visible:
                mx = obj.matrix_world

                coords = [(mx @ Vector(co))[int(self.axis)] for co in obj.bound_box]

                if min(coords) < 0 and max(coords) > 0:
                    obj.select_set(True)

        return {'FINISHED'}
