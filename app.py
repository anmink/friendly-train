from flask import Flask, request, jsonify
from rembg import remove
import numpy as np
from PIL import Image
import cv2
import os
import urllib.parse

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
    print('try start')
    #image = '/Users/anne/Library/Developer/CoreSimulator/Devices/9FF48E96-D0C1-401C-876B-58A3E766DBE6/data/Containers/Data/Application/483991C6-B38A-46A2-8DB6-DE00D6D55056/Library/Caches/ExponentExperienceData/%2540anonymous%252Fdressflow-1d3c3221-3739-4bb6-8c2b-6c7f07405045/IMG_4919.jpg'
    #image_path = 'file:///Users/anne/Library/Developer/CoreSimulator/Devices/9FF48E96-D0C1-401C-876B-58A3E766DBE6/data/Containers/Data/Application/483991C6-B38A-46A2-8DB6-DE00D6D55056/Library/Caches/ExponentExperienceData/%2540anonymous%252Fdressflow-1d3c3221-3739-4bb6-8c2b-6c7f07405045/Camera/FB01E267-FE0C-4D79-9BDF-031358DF9115.jpg'
    data = request.json
    image_path = data.get('image')
    print('print image_path post:', image_path)
    convert_uri_to_path(image_path)
    remove_background(image_path)
    return ('done post')
  except Exception as e:
    print('except')
    return jsonify({'error call': str(e)})
  
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port='8000')