import numpy as np
from flask import Flask, request, send_file, make_response
from PIL import Image
import matplotlib.pyplot as plt



from flask import Flask

app = Flask(__name__)



@app.route("/")
def sanity_check():
    return "<p>Servicio de generación de histogramas de imágenes corriendo correctamente</p>"


@app.route("/getHist", methods=['POST'])
def MakeNegative():
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