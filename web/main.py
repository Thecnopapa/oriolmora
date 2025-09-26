### IMPORTS ############################################################################################################

# ESSENTIAL IMPORTS
import json
import os

from openpyxl.worksheet import page

# BACKEND IMPORTS
from backend.utilities import *
from backend.variables import *

# WEB-RELATED IMPORTS
from flask import Flask, render_template, redirect, request, make_response, session, url_for, jsonify, \
    send_from_directory
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

### END IMPORTS ########################################################################################################


### APP CONFIG #########################################################################################################

print(" * Inititlising...")

app = Flask(__name__)
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APPLICATION_ROOT'] = APPLICATION_ROOT
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

app.secret_key = "TEST_KEY"

@app.before_request
def make_session_permanent():
    session.permanent = True

### END APP CONFIG #####################################################################################################


### CONTEXT IMPORTS ####################################################################################################

from backend.admin import *
from backend.database import *
from backend.pages import *

### END CONTEXT IMPORTS ################################################################################################



### BASE ROUTES ########################################################################################################

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return render_template("ERROR.html", code=e.code, name=e.name, description=e.description, request=request), e.code

@app.route("/static/<folder>/<file>")
@app.route("/static/<file>")
def get_static(file, folder=None):
    file = secure_filename(file)
    if folder is None:
        return send_from_directory("static", file)
    folder = secure_filename(folder)
    return send_from_directory("static", folder + "/" + file)

@app.route("/style/<file>")
def get_style(file):
    return redirect("/static/style/"+secure_filename(file))

@app.route("/scripts/<file>")
def get_script(file):
    return redirect("/static/scripts/"+secure_filename(file))
@app.route("/fonts/<file>")
def get_font(file):
    return redirect("/static/scripts/"+secure_filename(file))

# DEVELOPMENT
@app.route("/media/<file>")
def get_media(file):
    return redirect("/static/media/"+secure_filename(file))

### END BASE ROUTES ####################################################################################################


### PAGE ROUTES #############################################################################################################


app.add_url_rule("/", view_func=page_index)
app.add_url_rule("/<lan>", view_func=page_index)



### END PAGE ROUTES #########################################################################################################










### APP RUN ############################################################################################################

# DEVELOPMENT
def start_ngrok():
    from pyngrok import ngrok
    url = ngrok.connect(5000, name="tunnel1", url=NGROK_URL).public_url
    print(' * Tunnel URL:', url)

app.config["START_NGROK"] = os.environ.get('START_NGROK') == "1" and os.environ.get('WERKZEUG_RUN_MAIN') != 'true'

if app.config['START_NGROK']:
    start_ngrok()

# RUN
def main():
    app.run(port=5000, host="0.0.0.0", debug=False) # Not used if run from bash

if __name__ == "__main__":
    main()

### END APP RUN ########################################################################################################
