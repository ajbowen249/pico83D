bl_info = {
    'name': 'Pico 8 3D',
    'author': 'ajbowen249',
    'category': 'Import-Export',
    'version': (0, 0, 0),
    'blender': (2, 78, 0),
    'location': 'File > Export',
    'description': 'Mesh exporter for the Pico 8 3D Engine'
}

import bpy
import bmesh
import os
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

separator = ','

class ExportToPico83D(bpy.types.Operator, ExportHelper):
    '''Export Pico 8 3D'''
    bl_idname = 'export.pico83d'
    bl_label = 'Export Pico 8 3D'
    filename_ext = '.p83'

    just_selected = BoolProperty(name='Export Selected Meshes', description='Only export selected meshes', default=False)

    def execute(self, context):
        props = self.properties
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

        # make sure we're in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # gather meshes
        meshes = [obj.data for obj in bpy.context.scene.objects if obj.type == 'MESH' and (obj.select or not props.just_selected)]

        file = open(filepath, 'w')

        def write_num(num):
            file.write(str(round(num, 3)))

        def write_sep():
            file.write(separator)

        for mesh in meshes:
            # need to make sure we're working with triangles
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
            trimesh = bpy.data.meshes.new('%s_2' % mesh.name)
            bm.to_mesh(trimesh)
            bm.free()

            file.write(mesh.name)
            write_sep()
            write_num(len(trimesh.vertices))
            write_sep()
            write_num(len(trimesh.polygons))
            write_sep()

            # vertex values
            for vertex in trimesh.vertices:
                write_num(vertex.co.x)
                write_sep()
                write_num(vertex.co.y)
                write_sep()
                write_num(vertex.co.z)
                write_sep()

             # face indices
            for tri in trimesh.polygons:
                assert(len(tri.vertices) == 3)
                for index in tri.vertices:
                    write_num(index + 1) # Lua indieces are 1-based
                    write_sep()
                # todo, material
                file.write('12')
                write_sep()

            # normals
            for tri in trimesh.polygons:
                write_num(tri.normal.x)
                write_sep()
                write_num(tri.normal.y)
                write_sep()
                write_num(tri.normal.z)
                write_sep()

        file.flush()
        file.close()

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ExportToPico83D.bl_idname, text='Pico 8 3D (.p83)')

def register():
    bpy.utils.register_class(ExportToPico83D)
    bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ExportToPico83D)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == '__main__':
    register()
