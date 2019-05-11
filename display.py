import os
import argparse

from predict import *

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type = str, help = "Path to data")
parser.add_argument("--artist", type = str, help = "Name of the artist without spaces")

args = parser.parse_args()


data_path = args.data_path
artist = args.artist
predict(data_path, artist)

file = "rap.txt"
path = os.path.join(data_path,artist,file)
print("\n\nGenerating unique rap lyrics for",artist,"\n-------------------------------------------")
with open(path) as f:
	print(f.read())
