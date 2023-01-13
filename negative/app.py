import numpy as np
from flask import Flask, request, send_file, make_response
from PIL import Image, ImageOps


from flask import Flask

app = Flask(__name__)



@app.route("/")
def sanity_check():
    return "<p>Servicio de negativos de imágenes corriendo correctamente</p>"


@app.route("/getNegative", methods=['POST'])
def MakeNegative():
    #raw = np.fromstring(request.data, np.uint8).reshape(267,266)
    #
    #img = Image.fromarray(raw)
#
    #raw.flags.writeable = False
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream).convert(mode='RGB')
    

    negative = ImageOps.invert(img)
    negativeName = f'{hash(img.tobytes)}_negativo.png'
    negative.save(negativeName)
    
    out = [f'{str(i)}|' for i in negative.getdata()]
    out.append(negative.size[0])
    out.append(negative.size[1])
    return make_response(out, 200)

    return send_file(negativeName, mimetype='text/png')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)