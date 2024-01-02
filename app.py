from flask import Flask, request, jsonify
from rembg import remove

app = Flask(__name__)

print('hi')

def remove_background(image):
  print("start")
  input_path = 'input.png'
  output_path = 'output.png'

  with open(input_path, 'rb') as i:
      with open(output_path, 'wb') as o:
          input = i.read()
          output = remove(input)
          o.write(output)

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
  app.run(debug=True, host='0.0.0.0', port='8000')