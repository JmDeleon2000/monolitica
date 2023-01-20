import os
from flask import Flask, request, send_file

IMG_FOLDER = os.environ['IMG_VOL']

app = Flask(__name__)


@app.route('/<hash>/download', methods=['GET'])
def upload_file(hash):
    return send_file(f'{IMG_FOLDER}/{hash}.png', mimetype='png', as_attachment=True)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)