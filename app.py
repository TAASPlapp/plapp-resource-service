import uuid
import os
from flask import Flask, request, jsonify, make_response
from pathlib import Path

def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)
ensure_dir('assets')

app = Flask(__name__, static_folder='assets')

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/', methods=['GET', 'POST', 'PUT'])
def upload():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()

    file = request.files['file']
    filename = str(uuid.uuid1())
    file.save(os.path.join('assets', filename))
    path = f'https://plapp-resource-service.herokuapp.com/assets/{filename}'
    print(f'Saved file to: {path}')
    return path

@app.route('/assets/<path:path>', methods=['GET'])
def serve(path):
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    return app.send_static_file(path)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run()
