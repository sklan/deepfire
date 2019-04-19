import os
import random

import flask
from flask import request
from keras.models import load_model

from predict import generate_lyrics, compose_rap, vectors_into_song
from preprocess import *

path = '/Users/sklan/PyAiProjects/deepfire/data'
# 'jcole'
artists = ['kanye', 'eminem', 'tyler', 'snoop', 'asaprocky']
app = flask.Flask(__name__)

models = dict()


def get_models(path):
    for artist in artists:
        p = os.path.join(path, artist)
        models[artist] = load_model(os.path.join(p, 'model.h5'))
        models[artist]._make_predict_function()
    return models


@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = {"success": False}
    print(request.method)
    if request.method == "GET":
        artist = request.args.get('artist')

        if artist in artists:
            print(models[artist].summary())
            path = '/Users/sklan/PyAiProjects/deepfire/data'
            path = os.path.join(path, artist)
            with open(os.path.join(path, 'lyrics.txt'), mode='r') as f:
                text = f.read()
            lyrics = split_lyrics(text)
            initial_index = random.choice(range(len(lyrics) - 1))
            bars = generate_lyrics(text)
            with open(os.path.join(path, 'rhymes.txt'), mode='r') as f:
                rhymes_list = f.read()
            vectors = compose_rap(initial_index, lyrics, rhymes_list,
                                  models[artist])
            rap = vectors_into_song(vectors, bars, rhymes_list)
            data["predictions"] = ["\n".join(rap)]
            data["success"] = True
    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    get_models(path)
    app.run()
