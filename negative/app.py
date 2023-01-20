import hashlib
import os
from flask import Flask, request, send_file, redirect

from PIL import Image, ImageOps



app = Flask(__name__)

IMG_FOLDER = os.environ['IMG_VOL']
addr = 'http://download-service.labstranglerfig.svc.cluster.local:8000'

@app.route("/", methods=['GET', 'POST'])
def sanity_check():
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file.stream).convert(mode='RGB')


        negative = ImageOps.invert(img)
        negativeName = f'temp_negativo.png'
        negative.save(negativeName)


        with open(negativeName, 'rb') as f:
            hash = hashlib.sha256(f.read()).hexdigest()


        negative = Image.open(negativeName)
        negative.save(f'{IMG_FOLDER}{hash}.png')

        os.remove(negativeName)

        return redirect(f'{addr}/{hash}/download')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)