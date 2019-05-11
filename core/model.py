from keras.layers import LSTM
from keras.models import Sequential


def create_network(depth):
    model = Sequential()
    model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
    for i in range(depth):
        model.add(LSTM(8, return_sequences=True))
    model.add(LSTM(2, return_sequences=True))
    model.summary()
    model.compile(optimizer='rmsprop', loss='mse')
    return model
