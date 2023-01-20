
from __future__ import print_function
import requests

addr = 'http://127.0.0.1:8000'
test_url = addr + '/'

with (open('Original-standard-test-image-of-Mandrill-also-known-as-Baboon.png', 'rb')) as file:
    my_img = {'image': file}
    response = requests.post(test_url, files=my_img)


with open('Negativo.png', 'wb') as f:
    f.write(response.content)