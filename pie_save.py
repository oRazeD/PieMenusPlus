import bpy, os
from bpy.props import BoolProperty


class PIESPLUS_OT_batch_import(bpy.types.Operator):
    bl_idname = "pies_plus.batch_import"
    bl_label = "Batch Import"
    bl_description = "Batch import files based on a selected directory"
    bl_options = {'REGISTER'}

    import_type: bpy.props.EnumProperty(
        items=(
            ('fbx', "FBX", ""),
            ('obj', "OBJ", ""),
            ('both',"Both","")
        ),
        name='File Type'
    )

    include_subdirs: BoolProperty(
        name='Include Subdirectories',
        description='Include subdirectories of the selected directory'
    )

    group_into_colls: BoolProperty(
        name='Collection per Import',
        description='Create a new collection for every file imported and link them'
    )

    remove_uv_maps: BoolProperty(
        name='Clear UV Maps',
        description='Remove all UV Maps from all imported models'
    )

    # TODO for v1.4
    #
    #clear_normals: bpy.props.BoolProperty(
    #    name='Clear Normals',
    #    description='Clear custom normals from all imported models'
    #)

    directory: bpy.props.StringProperty()

    def settings_app(self,context):
        if self.remove_uv_maps:
            for ob in context.selected_objects:
                if ob.type == 'MESH':
                    context.view_layer.objects.active = ob

                    bpy.ops.mesh.uv_texture_remove()

    def new_coll(self,context):
        new_coll = bpy.data.collections.new(name = self.file_name[:-4])

        context.scene.collection.children.link(new_coll)

        context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[-1]

    def import_file(self, context):
        if self.import_type == 'fbx':
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".FBX"):
                    self.new_coll(context)

                    bpy.ops.import_scene.fbx(filepath=os.path.join(self.dir_name, self.file_name))

                    self.settings_app(context)

        elif self.import_type == 'obj':
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".OBJ"):
                    self.new_coll(context)

                    bpy.ops.import_scene.obj(filepath=os.path.join(self.dir_name, self.file_name))

                    self.settings_app(context)

        else: # Both
            for self.file_name in self.dir_contents:
                if self.file_name.upper().endswith(".FBX"):
                    self.new_coll(context)
                    
                    bpy.ops.import_scene.fbx(filepath=os.path.join(self.dir_name, self.file_name))

                    self.settings_app(context)

                if self.file_name.upper().endswith(".OBJ"):
                    self.new_coll(context)

                    bpy.ops.import_scene.obj(filepath=os.path.join(self.dir_name, self.file_name))

                    self.settings_app(context)

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


class PIESPLUS_OT_open_last(bpy.types.Operator):
    bl_idname = "pies_plus.open_last"
    bl_label = "Open Last"
    bl_description = "Opens the most recently opened file"
    bl_options = {'REGISTER'}

    def execute(self, context):
        recent_file_paths = bpy.utils.user_resource('CONFIG', "recent-files.txt")

        try:
            with open(recent_file_paths) as file:
                recent_files = file.read().splitlines()
        except (IOError, OSError, FileNotFoundError):
            recent_files = []

        if recent_files:
            most_recent = recent_files[0]

            bpy.ops.wm.open_mainfile(filepath=most_recent)
        return{'FINISHED'}


##############################
#   REGISTRATION
##############################


def register():
    bpy.utils.register_class(PIESPLUS_OT_batch_import)
    bpy.utils.register_class(PIESPLUS_OT_open_last)


def unregister():
    bpy.utils.unregister_class(PIESPLUS_OT_batch_import)
    bpy.utils.unregister_class(PIESPLUS_OT_open_last)


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
