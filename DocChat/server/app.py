import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from index_building import build, build_mock
from index_loading import run, run_mock

app = Flask(__name__)
app.config.from_pyfile('config.py')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'rtf', 'pptx'}
DIR_SEPARATOR = "/"
RESULTS = "results"
DOCS = "docs"

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def directory_for_client_id(clientId):
    return os.path.join(app.config['UPLOAD_FOLDER'], clientId)

def index_json_results_path_from_client_id(clientId):
    return os.path.join(directory_for_client_id(clientId), DOCS, RESULTS, "index.json")

def directory_for_client_id_documents(clientId):
    return os.path.join(directory_for_client_id(clientId), DOCS)

@app.route("/api/buildIndexForQuery", methods=["POST"])
def build_index():
    request_json = request.get_json()
    clientId = request_json.get('clientId')
    mock = request_json.get('mock')

    if mock == "useAPIKey":
        response = build(directory_for_client_id_documents(str(clientId)))
        return response
    else:
        response = build_mock(directory_for_client_id_documents(str(clientId)))
        return response


@app.route("/api/query", methods=["POST"])
def query_index():

    request_json = request.get_json()
    clientId = request_json.get('clientId')
    mock = request_json.get('mock')
    postQuery = request_json.get('query')

    if clientId is None:
        return

    index_file = index_json_results_path_from_client_id(str(clientId))

    if mock == "useAPIKey":
        if os.path.exists(index_file):
            response = run(postQuery, index_file)
            return response
        else:
            resp = jsonify({'message': 'no index.json for this client at /a/b/#/c/index.json'})
            resp.status_code = 400
    else:
        response = run_mock(postQuery, index_file)
        return response

    return resp


@app.route("/api/filesUpload", methods = ['POST'])
def pdfUploadPost():

    files = request.files.getlist('file')
    clientId = request.form.get('clientId')

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    if clientId == None:
        resp = jsonify({'message': 'No clientId sent'})
        resp.status_code = 400
        return resp

    # Create directory with id name if it doesn't exist
    directory = os.path.join(app.config['UPLOAD_FOLDER'])

    for file in files:
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            eventualPath = directory + DIR_SEPARATOR + clientId + DIR_SEPARATOR + DOCS
            if not os.path.exists(eventualPath):
                os.makedirs(eventualPath)

            final_full_path = os.path.join(eventualPath, filename)
            if(os.path.exists(final_full_path)):
                resp = jsonify({'message': 'file name exists'})
                resp.status_code = 200

            else: #file doesnt exist but path now does.
                file.save(os.path.join(eventualPath, filename))
                resp = jsonify({'message': 'saved file ' + os.path.join(eventualPath, filename)})
                resp.status_code = 201

        else:
            resp = jsonify({'message': 'Allowed file types are txt, pdf, rtf, ppt, pptx'})
            resp.status_code = 400
            return resp


    return resp

if __name__ == '__main__':
	app.run(port=8019, debug=True)
