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
import os
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

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

        file = open(filepath, 'w')
        file.write('some placeholder text')
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
