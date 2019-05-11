import argparse
import os

from model import create_network
from preprocess import *

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help='Path to training data',
                    default='data')
parser.add_argument("--artist", type=str, help='Artist name')

args = parser.parse_args()


def train(path, artist, epochs=5, depth=4):
    path = os.path.join(path, artist)
    with open(os.path.join(path, 'lyrics.txt'), mode='r') as f:
        text = f.read()
    bars = split_lyrics(text)
    rhyme_list = rhyme_index(bars)
    with open(os.path.join(path, 'rhymes.txt'), mode='w') as f:
        f.write('\n'.join(rhyme_list))
    model = create_network(depth=depth)
    x_train, y_train = build_dataset(bars, rhyme_list)
    model.fit(x_train, y_train, batch_size=2, epochs=epochs)
    model.save(os.path.join(path, 'model.h5'))


if __name__ == "__main__":
    data_path = args.data_path
    artist = args.artist
    train(data_path, artist)
