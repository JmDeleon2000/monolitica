
from __future__ import print_function
import requests
from PIL import Image
import numpy as np

addr = 'http://localhost:2510'
test_url = addr + '/getNegative'

with (open('Original-standard-test-image-of-Mandrill-also-known-as-Baboon.png', 'rb')) as file:
    my_img = {'image': file}
    response = requests.post(test_url, files=my_img)



data = response.text.replace('(',
 '').replace(')', 
 ',').replace('[', 
 '').replace(']', 
 '').replace('"', 
 '').split('|')

x = data[-1::][0]
size = [int(i) for i in x.split(',') if i != '']
data.pop()

raw = np.array([[int(j) for j in i.split(',') if j != ''] for i in data], dtype=np.uint8).reshape(size[1], size[0], 3)
img = Image.fromarray(raw)
img.save('Negativo.png')