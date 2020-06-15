import pymesh
import requests

import argparse
import numpy as np
from numpy.linalg import norm

import sys
import io
import time


from google.cloud import storage

# base_storage_url = "http://localhost:4000/graphql"  # TODO TEMP
base_storage_url = "https://ca5c14c10222.ngrok.io/graphql"  # TODO TEMP


def create_calc_mesh(geometry_id, file_format_out="ply"):
    trimesh, mesh_name = get_trimesh(geometry_id)
    # trimesh = pymesh.load_mesh(io.BytesIO(r.content))

    # Regenerating trimesh for calculation compliance
    trimesh = fix_mesh(trimesh, detail="low")
    trimesh.add_attribute("vertex_normal")
    trimesh.get_attribute("vertex_normal")
    trimesh.add_attribute("face_normal")
    trimesh.get_attribute("face_normal")

    cell_size = 100  ## TOOD should be fraction of total mesh size
    tetmesh = pymesh.tetrahedralize(trimesh, cell_size, with_timing=False)
    # tetmesh.add_attribute("face_normal")
    # tetmesh.get_attribute("face_normal")

    tri_filename = f"{int(time.time() * 1000)}_{mesh_name.split('.')[0][14:]}_tri.{file_format_out}"
    tet_filename = f"{int(time.time() * 1000)}_{mesh_name.split('.')[0][14:]}_tet.{file_format_out}"

    pymesh.meshio.save_mesh(tri_filename, trimesh, *trimesh.get_attribute_names())
    pymesh.meshio.save_mesh(tet_filename, tetmesh)

    client = storage.Client.from_service_account_json("FLINCKSolid-ed5cf9e81eb7.json")
    bucket = client.get_bucket("flinck-dev")

    tri_blob = bucket.blob(tri_filename)
    tet_blob = bucket.blob(tet_filename)
    # TODO don't create file, but filestream
    tri_blob.upload_from_filename(
        filename=tri_filename
    )
    tet_blob.upload_from_filename(
        filename=tet_filename
    )
    

    return tri_filename, tet_filename

def get_trimesh(geometry_id):
    query = """query geometry($geometry_id: String!){
            geometry(geometryId: $geometry_id){
            signedUrl
        }
    }
    """

    variables = {"geometry_id": geometry_id}
    r = requests.post(
        url=base_storage_url, json={"query": query, "variables": variables}
    )

    # TODO fix signedUrl
    # aquiring signedUrl
    mesh_url = r.json()["data"]["geometry"]["signedUrl"]
    test_url = mesh_url.split("/")
    mesh_name = test_url[4].split("?")[0]
    test_url = "https://storage.googleapis.com/" + test_url[3] + "/" + mesh_name
    new_url = "https://storage.googleapis.com/" + test_url
    # render_mesh_path = "1591733049157_ABSKG-40AL9_VAZPF-008_132S_76NO_102332978.stl"

    # Check for correct file format
    file_format_in = new_url.split(".")[-1].lower()
    assert file_format_in in ["stl"], "Incorrect file format loaded"

    # Downloading uploaded mesh
    r = requests.get(test_url, stream=True, allow_redirects=True)

    temp_file = f"temp_render_mesh.{file_format_in}"
    with open(temp_file, "wb") as f:
        f.write(r.content)    
    # io.BytesIO(r.content)
    trimesh = pymesh.load_mesh(temp_file)

    return trimesh, mesh_name

def fix_mesh(mesh, detail="normal"):
    bbox_min, bbox_max = mesh.bbox;
    diag_len = norm(bbox_max - bbox_min);
    if detail == "normal":
        target_len = diag_len * 5e-3;
    elif detail == "high":
        target_len = diag_len * 2.5e-3;
    elif detail == "low":
        target_len = diag_len * 1e-2;
    print("Target resolution: {} mm".format(target_len));

    count = 0;
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100);
    mesh, __ = pymesh.split_long_edges(mesh, target_len);
    num_vertices = mesh.num_vertices;
    while True:
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6);
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                preserve_feature=True);
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100);
        if mesh.num_vertices == num_vertices:
            break;

        num_vertices = mesh.num_vertices;
        print("#v: {}".format(num_vertices));
        count += 1;
        if count > 10: break;

    mesh = pymesh.resolve_self_intersection(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh = pymesh.compute_outer_hull(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5);
    mesh, __ = pymesh.remove_isolated_vertices(mesh);

    return mesh;