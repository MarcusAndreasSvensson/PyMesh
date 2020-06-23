import pymesh
import requests

from create_calc_mesh import get_trimesh

# mesh_url = "https://storage.googleapis.com/flinck-dev/1592060344393_ABSKG-40AL9_VAZPF-008_132S_76NO_102332978.stl?GoogleAccessId=flinck%40flincksolid.iam.gserviceaccount.com&Expires=1592942031&Signature=Ob5W60dC4naFKvgyUrowAJQM5cxCLAKdPYuc3UOPyo42Eu2%2FIZHO9YMTn3WOOSAFC6rhUzXpaFUvMLU6nkcFkHSBwoUqh0YboB5m1fFm4yUc%2BzQiwOU4Lcab8fVPQY3OWhUAwDjHWz4xlFoSIskwCzJOn%2B4z6QvnknCE2JFHc1OuYNihVaaK7dCCRBNoyqZxRz9TbVRG%2BjqBlYfURLBihrw9YWVHLW7lgExnleBnPFOXLGeyTw5A%2FtYwNJjAEJ0K3P9k%2FXXQjMdM6KYTtNkW1CDUjvRl9Dymf3YCw0hXRAqI7%2F5S5EUTVgQZYqMEp0eDQNa6swApjpzK9TdSpcWvEw%3D%3D"

geometry_id = "cf38ba38-fc55-44b3-b63b-e17fdca42677"

trimesh, mesh_name = get_trimesh(geometry_id)

trimesh = fix_mesh(trimesh, detail="low")
