import bpy
import inspect, logging, bmesh
from timeit import default_timer
import bpy.types as types

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class OpInfo: # Mix-in class
    bl_options = {'REGISTER', 'UNDO'}
    bl_label = ""


class CodeTimer(object):
    '''A basic context manager for timing code blocks'''
    def __init__(self, repeat: int=100):
        self.timing = 1000 # milliseconds
        self.timer = default_timer
        self.repeat = repeat

    def __enter__(self):
        self.start = self.timer()
        return self.repeat

    def __exit__(self, _exc_type, _exc_val, _traceback):
        end = self.timer()
        self.elapsed = (end - self.start) * self.timing

        print(f"{inspect.stack()[1][3]}'s time: {round(self.elapsed, 6)}ms")


class BMeshFromEditMode():
    '''Generate a temporary BMesh. Accepts Objects or Meshes as inputs temp change'''
    def __init__(self, input_data: types.Object | types.Mesh, update_mesh: bool=True): # TODO Should accept lists?
        if isinstance(input_data, types.Mesh):
            self.input_data = input_data
        else:
            self.input_data = input_data.data

        self.update_mesh = update_mesh

    def __enter__(self):
        self.bm = bmesh.from_edit_mesh(self.input_data)
        return self.bm

    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        # NOTE do not use self.bm.free() for BMeshes made in Edit Mode, uses same data regardless

        if self.update_mesh:
            bmesh.update_edit_mesh(self.input_data)


def get_addon_preferences():
    package_name = __name__.partition('.')[0]
    return bpy.context.preferences.addons[package_name].preferences
