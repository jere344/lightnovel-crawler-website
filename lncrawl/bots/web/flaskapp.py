from flask import Flask, send_file, send_from_directory
from .lib import LIGHTNOVEL_FOLDER
import pathlib

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/favicon.ico")
def favicon():
    return send_file("static/assets/favicon.png", mimetype="image/x-icon")


@app.route("/image/<path:file>")
def image(file):
    path: pathlib.Path = LIGHTNOVEL_FOLDER / file
    if path.exists() and path.name == "cover.jpg":
        return send_from_directory(LIGHTNOVEL_FOLDER, file)
    else:
        print(path)
        print(path.name)


# --------------------------------------------------------------

# @app.route()
# ----------------------------------------------------------------------------------------------------------------------


# @app.route("/lncrawl/download/<int:id>/")
# @app.route("/lncrawl/download/<int:id>/<string:job_id>")
# def download():
#     data = request.json
#     pass


# @app.route("/lncrawl/status/<string:job_id>")
# def job_status(job_id):
#     pass


# @app.route("/lncrawl/cancel/<string:job_id>")
# def cancel_job(job_id):
#     pass


# @app.route("/lncrawl/list")
# def list_downloaded():
#     pass
