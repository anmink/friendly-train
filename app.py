from flask import Flask, request, jsonify
from rembg import remove
import numpy as np
from PIL import Image
import cv2
import os
import urllib.parse
import base64

app = Flask(__name__)

print('hi')

def convert_uri_to_path(uri):
  path = urllib.parse.urlparse(uri).path

  if path.startswith("/"):
      path = path[1:]

  decoded_path = urllib.parse.unquote(path)
  print("Konvertierter Pfad:", decoded_path)
  return decoded_path


def remove_background(image):
  input_path = image[7:]
  print('rembg', input_path)
  output_path = 'file:///var/mobile/Containers/Data/Application/EB7F7691-6BE9-48A6-A9F9-93FA70E0DB45/Library/Caches/ExponentExperienceData/%2540anonymous%252Fdressflow-1d3c3221-3739-4bb6-8c2b-6c7f07405045/out.png'

  input = Image.open(input_path)
  print('after input')
  output = remove(input)
  output.save(output_path)
  print('done in rembg')
  return output

@app.route('/', methods=['GET'])
def get():
  return ('hello world in get')

@app.route('/remove', methods=['POST'])
def image_processing():
  try:
    image_base64 = request.get_data()
    print('image_base64 worked', image_base64)
    #image_bytes = base64.b64decode(image_base64)
    #print('image_bytes worked')
    removed_background_data = remove(image_base64)
    print('removed worked')

    removed_background_base64 = base64.b64encode(removed_background_data).decode('utf-8') + '.png'
    #print(removed_background_base64)
    return jsonify({'removed_background': removed_background_base64})
  except Exception as e:
    return jsonify({'error': str(e)}), 500
  
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port='10000')