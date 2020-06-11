from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)


######### Mesh #########


@app.route(
    "/", methods=["GET"],
)
@cross_origin()
def mesh_converter(mesh_id):
    # TODO Check for input type
    # gs_filename = convert_mesh(mesh_id)

    # return jsonify({"gsFilename": gs_filename})
    return jsonify({"gsFilename": "OMG DET FUNKAR"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)
