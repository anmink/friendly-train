from flask import Flask, request, jsonify
from rembg import remove
import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model
from keras.applications.resnet import preprocess_input
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

print('hi')
model = None 

def load_model_once():
    global model
    print('does something')
    model = load_model('model.h5')
    print('model loaded')  # Laden Sie Ihr gespeichertes Modell hier


@app.route('/', methods=['GET'])
def get():
  load_model_once()
  return ('hello world in get')

@app.route('/remove', methods=['POST'])
def image_processing():
  print('moin')
  image_base64 = request.get_data()
  print('image_base64 worked')
  image_bytes = base64.b64decode(image_base64)
  print('image_bytes worked')
  removed_background_data = remove(image_bytes)
  print('removed worked')

  removed_background_base64 = base64.b64encode(removed_background_data)
  image_base64 = removed_background_base64
  print('worked till here')

  # Dekodieren Sie den Base64-String in ein Bild
  image = decode_base64_to_image(image_base64)
  image = cv2.resize(image, (224, 224))  # Größe entsprechend Ihrem Modell anpassen
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = preprocess_input(image)
  image = np.expand_dims(image, axis=0)
  print('image', image)
  # Vorhersage durchführen
  article_pred, color_pred = model.predict(image)

  with open('labels.json', 'r') as f:
      labels = json.load(f)

  # Bestimmen der Klasse mit der höchsten Wahrscheinlichkeit für article
  article_class_index = np.argmax(article_pred)
  article_predicted_class = labels['article_labels'][article_class_index]

  # Bestimmen der Klasse mit der höchsten Wahrscheinlichkeit für color
  color_class_index = np.argmax(color_pred)
  color_predicted_class = labels['color_labels'][color_class_index]

  print("Predicted article class:", article_predicted_class)
  print("Predicted color class:", color_predicted_class)

  data = removed_background_base64, color_predicted_class

  return json.dumps({
     'image': removed_background_base64.decode('utf-8'),
     'type': article_predicted_class,
     'color': color_predicted_class
  })
  

def decode_base64_to_image(base64_string):
  # Entfernen Sie das Präfix 'data:image/jpeg;base64,' und dekodieren Sie den Base64-String
  #encoded_data = base64_string.split(',')[1]
  nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)
  image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  return image
  
if __name__ == '__main__':
  app.run(debug=True, host='192.168.2.177', port='8082')
  #fuer render port=10000