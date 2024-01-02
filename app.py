from flask import Flask, request, jsonify
from rembg import remove
from flask_cors import CORS
from PIL import Image
import cv2

app = Flask(__name__)
CORS(app)

print('hi')

def remove_background(image):
    print('start')
    input_path = image
    updated_input_path = input_path[7:]
    output_path = '/Users/anne/Desktop/Ordner/Code/dressflow/images'
    print(updated_input_path)
    input = cv2.imread(updated_input_path)
    print('failed')
    output = remove(input)
    cv2.imwrite(output_path, output)

@app.route('/', methods=['GET'])
def get():
  return ('hello world in get')

@app.route('/remove', methods=['POST'])
def image_processing():
  try:
    data = request.json
    image = data.get('image')
    remove_background(image)
    print(image)
    return ('work done')
  except Exception as e:
    print('except')
    return jsonify({'error': str(e)})
  
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')