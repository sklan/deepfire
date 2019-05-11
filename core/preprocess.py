import re

import markovify
import numpy as np
import pronouncing


def split_lyrics(text):
    text = text.split("\n")
    while "" in text:
        text.remove("")
    return text


def markov(text):
    markov_model = markovify.NewlineText(text)
    return markov_model


def rhyme_index(bars):
    rhymes = []
    for i in bars:
        # Take the last word from each bar
        word = re.sub(r"\W+", '', i.split(" ")[-1]).lower()
        rhymes_list = set(pronouncing.rhymes(word))

        # A list that stores the last two letters of each rhyme of a word.
        rhymes_ends = [i[-2:] for i in rhymes_list]

        if rhymes_ends:
            rhyme_scheme = max(set(rhymes_ends), key=rhymes_ends.count)
            rhymes.append(rhyme_scheme[::-1])
    rhymes = sorted(set(rhymes))
    return rhymes


def rhyme(line, rhyme_list):
    rhymes = []
    word = re.sub(r"\W+", '', line.split(" ")[-1]).lower()
    rhymes_list = pronouncing.rhymes(word)
    rhymes_ends = [i[-2:] for i in rhymes_list]
    if rhymes_ends:
        rhyme_scheme = max(set(rhymes_ends), key=rhymes_ends.count)
        rhymes.append(rhyme_scheme)
        try:
            float_rhyme = rhyme_list.index(rhyme_scheme)
            float_rhyme = float_rhyme / float(len(rhyme_list))
            return float_rhyme
        except:
            pass
    return 0.


def syllables(line, max_syllables=16):
    count = 0
    for word in line.split(" "):
        vowels = 'aeiouy'
        word = word.lower().strip(".:;?!")
        if word != '' and word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
    return int(count / max_syllables)


def build_dataset(bars, rhyme_list):
    dataset = []
    for line in bars:
        dataset.append([line, syllables(line), rhyme(line, rhyme_list)])

    x_train = []
    y_train = []

    for i in range(len(dataset) - 3):
        lines = dict()
        for j in range(i, i + 4):
            lines.update({j - i + 1: dataset[j][1:]})
        x = [lines[1][0], lines[1][1], lines[2][0], lines[2][1]]
        x = np.array(x)
        x = x.reshape(2, 2)
        x_train.append(x)
        y = [lines[3][0], lines[3][1], lines[4][0], lines[4][1]]
        y = np.array(y)
        y = y.reshape(2, 2)
        y_train.append(y)

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    return x_train, y_train
