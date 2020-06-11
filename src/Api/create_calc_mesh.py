import pymesh
import requests


def create_calc_mesh(signedUrl):
    render_mesh_path = "1591733049157_ABSKG-40AL9_VAZPF-008_132S_76NO_102332978.stl"
    mesh = pymesh.load_mesh(render_mesh_path)

    cell_size = 0.1  ## TOOD should be fraction of total mesh size
    pymesh.tetrahedralize(mesh, cell_size)

    return "HAHAHA"