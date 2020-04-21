import uuid
import os
from flask import Flask, request, jsonify
from pathlib import Path

def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)
ensure_dir('assets')

app = Flask(__name__, static_folder='assets')

@app.route('/', methods=['GET', 'POST', 'PUT'])
def upload():
    print(request.get_json())
    file = request.files['file']
    filename = str(uuid.uuid1())
    file.save(os.path.join('assets', filename))
    return f'https://plapp-resource-service.herokuapp.com/assets/{filename}'

@app.route('/assets/<path:path>', methods=['GET'])
def serve(path):
    return app.send_static_file(path)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
    
if __name__ == '__main__':
    app.run()
