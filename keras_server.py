import os
import random

import flask
from flask import request
from keras.models import load_model

from predict import generate_lyrics, compose_rap, vectors_into_song
from preprocess import *


def get_model(path):
    model = load_model(os.path.join(path, 'model.h5'))
    return model


path = '/Users/sklan/PyAiProjects/deepfire/data'

artists = ['kanye', 'eminem', 'tyler', 'snoop', 'asaprocky', 'jcole']
app = flask.Flask(__name__)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = {"success": False}
    print(request.method)
    if request.method == "GET":
        artist = request.args.get('artist')

        if artist in artists:
            path = '/Users/sklan/PyAiProjects/deepfire/data'
            path = os.path.join(path, artist)
            model = get_model(path)
            with open(os.path.join(path, 'lyrics.txt'), mode='r') as f:
                text = f.read()
            lyrics = split_lyrics(text)
            initial_index = random.choice(range(len(lyrics) - 1))
            bars = generate_lyrics(text)
            with open(os.path.join(path, 'rhymes.txt'), mode='r') as f:
                rhymes_list = f.read()
            vectors = compose_rap(initial_index, lyrics, rhymes_list, model)
            rap = vectors_into_song(vectors, bars, rhymes_list)
            data["predictions"] = ["\n".join(rap)]
            data["success"] = True
    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))

    app.run()
