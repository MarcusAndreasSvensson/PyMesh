from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from create_calc_mesh import create_calc_mesh

app = Flask(__name__)


######### Mesh #########


@app.route(
    "/<string:geometry_id>", methods=["GET"],
)
@cross_origin()
def mesh_converter(geometry_id):
    # TODO Check for input type
    gs_filename = create_calc_mesh(geometry_id)

    return jsonify({"gsFilename": gs_filename})
    # return jsonify({"gsFilename": "OMG DET FUNKAR"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)
