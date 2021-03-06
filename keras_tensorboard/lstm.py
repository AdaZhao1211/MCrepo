import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Activation
from keras.utils.data_utils import get_file
from keras.optimizers import RMSprop
import numpy as np
import random
import argparse
import sys
import tensorflow as tf

from utils import sample
FLAGS = None
def train():
    path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
    text = open(path).read().lower()  # read the file and convert to lowercase
    chars = sorted(list(set(text)))
    char_indices = dict((c,i) for i, c in enumerate(chars))
    indices_char = dict((i,c) for i,c in enumerate(chars))
    maxlen = 40
    sentences= []
    next_chars=[]

    for i in range(0, len(text)-maxlen, 3):
        sentences.append(text[i:i+maxlen])
        next_chars.append(text[i+maxlen])
    X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]]=1
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))
    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    #actual traininig
    #create a tensorboard object called history
    history = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
    #add callbacks to fit()
    model.fit(X, y, batch_size=128, epochs=20, callbacks=[history])
    start_index = random.randint(0, len(text)-maxlen-1)

    for diversity in [0.2, 0.5, 1.0, 1.2]:

        generated = ''
        sentence = text[start_index: start_index+maxlen] #randomly picking 40 chars for my seed
        generated+=sentence
        print('MY SEED IS', sentence)
        sys.stdout.write(generated)

        for i in range(400):

            x = np.zeros((1, maxlen, len(chars)))
            for t,char in enumerate(sentence):
                x[0,t,char_indices[char]]=1

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
            sys.stdout.write(next_char)
            sys.stdout.flush()
def main(_):
  train()

if __name__ == '__main__':
  tf.app.run(main=main, argv=[sys.argv[0]])
