import os
import random
import argparse

from keras.models import load_model
from preprocess import *

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help='Path to training data')
parser.add_argument("--artist", type=str, help='Artist name')

args = parser.parse_args()


def generate_lyrics(text):
    bars = []
    last_words = []
    lyrics_length = len(text.split('\n'))
    count = 0
    markov_model = markov(text)

    while len(bars) < lyrics_length / 9 and count < lyrics_length * 2:
        bar = markov_model.make_sentence()
        if bar is not None and syllables(bar) < 1:
            last_word = re.sub(r"\W+", '', bar.split(" ")[-1]).lower()
            if bar not in bars and last_words.count(last_word) < 3:
                bars.append(bar)
                last_words.append(last_word)
                count += 1
    return bars


def compose_rap(random_number, lyrics, rhymes_list, model):
    rap_vectors = []
    initial_lines = lyrics[random_number:random_number + 8]

    starting_input = []
    for line in initial_lines:
        starting_input.append([syllables(line), rhyme(line, rhymes_list)])

    starting_vectors = model.predict(
        np.array([starting_input]).flatten().reshape(4, 2, 2))
    rap_vectors.append(starting_vectors)

    for i in range(49):
        rap_vectors.append(model.predict(
            np.array([rap_vectors[-1]]).flatten().reshape(4, 2, 2)))
    return rap_vectors


def vectors_into_song(vectors, generated_lyrics, rhyme_list):
    def last_word_compare(rap, line2):
        penalty = 0
        for line1 in rap:
            word1 = line1.split(" ")[-1]
            word2 = line2.split(" ")[-1]
            while word1[-1] in "?!,. ":
                word1 = word1[:-1]

            while word2[-1] in "?!,. ":
                word2 = word2[:-1]

            if word1 == word2:
                penalty += 0.2

        return penalty

    def calculate_score(vector_half, syllables, rhyme, penalty,
                        max_syllables=16):
        desired_syllables = vector_half[0]
        desired_rhyme = vector_half[1]
        desired_syllables = desired_syllables * max_syllables
        desired_rhyme = desired_rhyme * len(rhyme_list)

        score = 1.0 - (abs((float(desired_syllables) - float(syllables))) + abs(
            (float(desired_rhyme) - float(rhyme)))) - penalty

        return score

    dataset = []
    for line in generated_lyrics:
        line_list = [line, syllables(line), rhyme(line, rhyme_list)]
        dataset.append(line_list)

    rap = []

    vector_halves = []
    for vector in vectors:
        vector_halves.append(list(vector[0][0]))
        vector_halves.append(list(vector[0][1]))

    for vector in vector_halves:
        scorelist = []
        for item in dataset:
            line = item[0]

            if len(rap) != 0:
                penalty = last_word_compare(rap, line)
            else:
                penalty = 0
            total_score = calculate_score(vector, item[1], item[2], penalty)
            score_entry = [line, total_score]
            scorelist.append(score_entry)

        fixed_score_list = []
        for score in scorelist:
            fixed_score_list.append(float(score[1]))
        max_score = max(fixed_score_list)
        for item in scorelist:
            if item[1] == max_score:
                rap.append(item[0])

                for i in dataset:
                    if item[0] == i[0]:
                        dataset.remove(i)
                        break
                break
    return rap


def predict(path, artist):
    path = os.path.join(path, artist)
    model = load_model(os.path.join(path, 'model.h5'))
    with open(os.path.join(path, 'lyrics.txt'), mode='r') as f:
        text = f.read()
    lyrics = split_lyrics(text)
    initial_index = random.choice(range(len(lyrics) - 1))
    bars = generate_lyrics(text)
    with open(os.path.join(path, 'rhymes.txt'), mode='r') as f:
        rhymes_list = f.read()
    vectors = compose_rap(initial_index, lyrics, rhymes_list, model)
    rap = vectors_into_song(vectors, bars, rhymes_list)
    with open(os.path.join(path, 'rap.txt'), "w") as f:
        for bar in rap:
            f.write(bar)
            f.write("\n")


if __name__ == "__main__":
    data_path = args.data_path
    artist = args.artist
    predict(data_path, artist)
