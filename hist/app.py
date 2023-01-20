import hashlib
import os
from flask import Flask, request, send_file, make_response
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


from flask import Flask

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def sanity_check():
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file.stream).convert(mode='RGB')

        red     = []
        green   = []
        blue    = []

        for i in np.array(img):
            for j in i:
                red.append(j[0])
                green.append(j[1])
                blue.append(j[2])

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        ax1.hist(red,     bins=20, color='red'    )
        ax2.hist(green,   bins=20, color='green'  )
        ax3.hist(blue,    bins=20, color='blue'   )
        ax1.set_title('Rojo')
        ax2.set_title('Verde')
        ax3.set_title('Azul')

        fig.tight_layout()
        fig_name = f'fig.png'
        plt.savefig(fig_name)


        with open(fig_name, 'rb') as f:
            hash = hashlib.sha256(f.read()).hexdigest()


        hist = Image.open(fig_name)
        hist.save(f'{hash}.png')

        os.remove(fig_name)

        return send_file(f'{hash}.png', mimetype='png')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>'''

@app.route("/getHist", methods=['POST'])
def Makehist():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream).convert(mode='RGB')

    red     = []
    green   = []
    blue    = []

    for i in np.array(img):
        for j in i:
            red.append(j[0])
            green.append(j[1])
            blue.append(j[2])
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.hist(red,     bins=20, color='red'    )
    ax2.hist(green,   bins=20, color='green'  )
    ax3.hist(blue,    bins=20, color='blue'   )
    ax1.set_title('Rojo')
    ax2.set_title('Verde')
    ax3.set_title('Azul')

    fig.tight_layout()
    fig_name = f'fig.png'
    plt.savefig(fig_name)

    img = Image.open(fig_name).convert(mode='RGB')
    out = [f'{str(i)}|' for i in img.getdata()]
    out.append(img.size[0])
    out.append(img.size[1])

    return make_response(out, 200)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)