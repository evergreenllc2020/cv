from __future__ import print_function
from flask import Flask, request, render_template,send_from_directory
from keras import regularizers
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import Dropout
from keras.layers import GlobalAveragePooling2D
from keras.layers import BatchNormalization
from keras.layers import Activation,Dense
from keras.models import Sequential,load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.applications.inception_v3 import InceptionV3
from os import listdir
import os
from os.path import isfile, join
import os, re, os.path
import numpy as np
import pandas as pd
from numpy.random import rand
from keras.callbacks import ModelCheckpoint
# Scikit Imports
from sklearn.model_selection import train_test_split
# Matplot Imports
import matplotlib.pyplot as plt
from keras.models import model_from_json
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import keras.backend.tensorflow_backend as tb

tb._SYMBOLIC_SCOPE.value = True


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
MODEL_JSON_PATH = "/Volumes/My Passport for Mac/model/dogs-vs-cats.json"
MODEL_H5_PATH = "/Volumes/My Passport for Mac/model/dogs-vs-cats.h5"
LABELS_PATH = "/Volumes/My Passport for Mac/data/dogs-vs-cats/labels.csv"


# setting up template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=TEMPLATE_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app = Flask(__name__)

def clear_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))

def read_csv(filepath):
     if os.path.splitext(filepath)[1] != '.csv':
          return  # or whatever
     seps = [',', ';', '\t']                    # ',' is default
     encodings = [None, 'utf-8', 'ISO-8859-1']  # None is default
     for sep in seps:
         for encoding in encodings:
              try:
                  return pd.read_csv(filepath, encoding=encoding, sep=sep)
              except Exception:  # should really be more specific 
                  pass
     raise ValueError("{!r} is has no encoding in {} or seperator in {}"
                      .format(filepath, encodings, seps))

def get_x_test(img_path, img_height, img_width):
    return np.array([img_to_array(load_img(img_path, target_size=(img_height, img_width)))]).astype('float32')

def predictInternal(x_test, model):
    #x_test = kimage.resize(image, 299, 299) 
    x_test /= 255.0
    test_predictions = model.predict(x_test)
    predictions = pd.DataFrame(test_predictions, columns=labels_ohe_names.columns)
    predictions = list(predictions.idxmax(axis=1))
    return predictions

def getImagesFilePathsFromFolder(path):
    onlyfiles = [ join(path,f) for f in listdir(path) if ( isfile(join(path, f)) and (".jpg" in f) )]
    return onlyfiles


	

def predict():
    fileCount = len(getImagesFilePathsFromFolder(UPLOAD_FOLDER)) 
    #print(getImagesFilePathsFromFolder(path))
    fig, ax = plt.subplots(1,fileCount, figsize=(50,50))
    img_Counter=0;
    output = {}
    for img_path in getImagesFilePathsFromFolder(UPLOAD_FOLDER):
        print(img_path)
        image_url = 'http://127.0.0.1:8000/uploads/' + img_path.split("/")[-1]
        #image_url = image_url[:-2]
        print(image_url)
        category = predictInternal(get_x_test(img_path, 150, 150), loaded_model)[0]
        print(category)
        output[image_url] = category 
        #ax[img_Counter].set_title(breed)
        #ax[img_Counter].imshow(load_img(img_path, target_size=(299, 299)))
        #img_Counter = img_Counter + 1
    return output

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        print("clearing upload dir")
        clear_dir(UPLOAD_FOLDER)
        print("done")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output = predict()
            if not (output is None):
                for imageUrl,category in output.items():
                    print(imageUrl)
                    print(category)
            return render_template('classifydogsandcats.html' ,output=output)
    else:
    	return render_template('classifydogsandcats.html', output=None)


labels_ohe_names = read_csv(LABELS_PATH)
# load json and create model
json_file = open(MODEL_JSON_PATH, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(MODEL_H5_PATH)
print("Loaded model from disk")
# evaluate loaded model on test data
loaded_model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy']) 
print("compiled model ")


@app.route("/")
def hello():
	return TEMPLATE_DIR

@app.route('/uploads/<filename>/')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/upload",	 methods=['GET', 'POST'])
def rec():
	return upload_file()



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000, debug=False, threaded=False)


