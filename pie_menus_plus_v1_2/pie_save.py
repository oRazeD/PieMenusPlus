import bpy
import os


class PIESPLUS_OT_batch_import(bpy.types.Operator):
    bl_idname = "pies_plus.batch_import"
    bl_label = "Batch Import"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    import_type: bpy.props.EnumProperty(items=(('fbx', "FBX", ""),
                                               ('obj', "OBJ", ""),
                                               ('both',"Both","")), name = 'File Type')

    include_subdirs: bpy.props.BoolProperty(default = False, name = 'Include Subdirectories')

    clear_normals: bpy.props.BoolProperty(default = False, name = 'Clear Normals')

    remove_uv_maps: bpy.props.BoolProperty(default = False, name = 'Clear UV Maps')

    group_into_colls: bpy.props.BoolProperty(default = False, name = 'Collection per Import', description = 'Create a new collection for every file imported and link them')

    directory: bpy.props.StringProperty()

    def new_coll(self,context):
        new_coll = bpy.data.collections.new(name = self.file_name[:-4])

        context.scene.collection.children.link(new_coll)

        context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[-1]

        for ob in context.selected_objects:
            new_coll.objects.link(ob)

            context.scene.collection.objects.unlink(ob)

    def import_file(self, context):
        if self.import_type == 'fbx':
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".FBX"):
                    bpy.ops.import_scene.fbx(filepath=os.path.join(self.dir_name, self.file_name))

                    if self.group_into_colls:
                        self.new_coll(context)

        elif self.import_type == 'obj':
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".OBJ"):
                    bpy.ops.import_scene.obj(filepath=os.path.join(self.dir_name, self.file_name))

                    if self.group_into_colls:
                        self.new_coll(context)

        else: # Both
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".FBX"):
                    bpy.ops.import_scene.fbx(filepath=os.path.join(self.dir_name, self.file_name))

                    if self.group_into_colls:
                        self.new_coll(context)
                    
                if self.file_name.upper().endswith(".OBJ"):
                    bpy.ops.import_scene.obj(filepath=os.path.join(self.dir_name, self.file_name))

                    if self.group_into_colls:
                        self.new_coll(context)

    def execute(self, context):
        if self.include_subdirs:
            self.dir_path = os.walk(self.directory)

            # Get a list of every subdirectory
            dir_list = [x[0] for x in self.dir_path]

            # Access every folders contents
            for self.dir_name in dir_list:
                self.dir_contents = os.listdir(self.dir_name)

                self.import_file(context)
        else:
            self.dir_contents = os.listdir(self.directory)

            self.dir_name = self.directory
            
            self.import_file(context)
        return{'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


##############################
#   REGISTRATION
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_batch_import)

def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_batch_import)


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####