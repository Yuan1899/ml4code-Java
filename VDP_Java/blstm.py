from __future__ import print_function

import warnings


import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.utils import compute_class_weight
from keras.layers.core import Masking
from tensorflow.keras.callbacks import TensorBoard
# tensorboard --logdir logs/

warnings.filterwarnings("ignore")

import numpy as np
import time

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional, LeakyReLU
from keras.optimizers import Adamax

from sklearn.model_selection import train_test_split

tf.autograph.set_verbosity(2)

# NAME = "TEST-{}".format(int(time.time()))
# tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))


"""
Bidirectional LSTM neural network
Fixed parameters from the VulDeePecker paper:
    Batch size: 64
    Dropout: 0.5
    Optimizer: Adamax
    Nodes: 300
    Epochs: 4
"""

# Values customizable for testing
batch_size = 64
dropout = 0.5
nodes = 300
epochs = 4

class BLSTM:
    def __init__(self, data, resampling_negative, resampling_positive, reweighting, layers, loss, name):

        print(data.shape)
        rows = data.shape[0]

        # To speed up intermediate testing, else condition should be used for proper runs
            
        rows_max = 999999999
        test_rows = 10000

        if rows > rows_max:
            labels = data.iloc[:test_rows, 1].values
            vectors = np.stack(data.iloc[:test_rows, 0].values)
            print("Warning: running with only a subset of rows")
        else:
            labels = data.iloc[:, 1].values
            vectors = np.stack(data.iloc[:, 0].values)

        # print(vectors.shape)

        positive_idxs = np.where(labels == 1)[0]
        negative_idxs = np.where(labels == 0)[0]
        
        print("---------------")
        print("Original positive samples: ", len(positive_idxs), resampling_positive)
        print("Original negative samples: ", len(negative_idxs), resampling_negative)

        # resampled_negative_idxs=negative_idxs
        # resampled_positive_idxs=positive_idxs

        resampled_negative_idxs = np.random.choice(negative_idxs, int(resampling_negative*(len(negative_idxs))), replace=False)
        resampled_positive_idxs = np.random.choice(positive_idxs, int(resampling_positive*(len(positive_idxs))), replace=False)
        resampled_idxs = np.concatenate([resampled_positive_idxs, resampled_negative_idxs])
        
        print("Resamples positive samples: ", len(resampled_positive_idxs))
        print("Resampled negative samples: ", len(resampled_negative_idxs))
        print("------------")

        X_train, X_test, y_train, y_test = train_test_split(vectors[resampled_idxs, ], labels[resampled_idxs],
                                                            test_size=0.2, stratify=labels[resampled_idxs])

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = to_categorical(y_train)
        self.y_test = to_categorical(y_test)

        self.name = name
        self.reweighting = reweighting
        self.batch_size = batch_size
        self.epochs = epochs
        class_weight = compute_class_weight(class_weight='balanced', classes=[0, 1], y=labels)
        self.class_weight = {i : class_weight[i] for i in range(2)}
        
        model = Sequential()

        # SySeVR uses masking, but it doesn't seem to change the result here
        # model.add(Masking(mask_value=0, input_shape=(vectors.shape[1], vectors.shape[2])))
        # model.add(Masking(mask_value=0, input_shape=X_train.shape[1:]))

        for i in range(layers):
            model.add(Bidirectional(LSTM(units=nodes, activation='tanh', recurrent_activation='sigmoid', return_sequences=True)))
            model.add(Dropout(dropout))

        model.add(Bidirectional(LSTM(units=nodes, activation='tanh', recurrent_activation='sigmoid')))
        model.add(Dropout(dropout))

        model.add(Dense(2, activation='sigmoid'))

        model.compile(optimizer='adamax', loss=loss, metrics=['accuracy', tf.keras.metrics.BinaryAccuracy()])
        # model.compile(optimizer='adamax', loss='binary_crossentropy',
                      # metrics=[tf.keras.metrics.TruePositives(), tf.keras.metrics.FalsePositives(),
                               # tf.keras.metrics.FalseNegatives(), tf.keras.metrics.Precision()])
        self.model = model


    """
    Trains model based on training data
    """

    # verbose=2

    def train(self):

        tensorboard = TensorBoard(log_dir='logs/{}'.format(self.name))

        # self.model.fit(x=self.X_train, y=self.y_train, validation_data=self.y_test, batch_size=self.batch_size, epochs=4, class_weight=self.class_weight)
        if self.reweighting:
            self.model.fit(self.X_train, self.y_train, epochs=self.epochs, validation_data=(self.X_test, self.y_test), batch_size=self.batch_size, class_weight=self.class_weight, callbacks=[tensorboard])
        else:
            self.model.fit(self.X_train, self.y_train, epochs=self.epochs, validation_data=(self.X_test, self.y_test), batch_size=self.batch_size, callbacks=[tensorboard])

        self.model.save_weights("models/" + self.name + "_model.h5")

    """
    Tests accuracy of model based on test data
    Loads weights from file if no weights are attached to model object
    """
    def test(self):
        self.model.load_weights("models/" +  self.name + "_model.h5")
        values = self.model.evaluate(self.X_test, self.y_test, batch_size=self.batch_size)
        predictions = (self.model.predict(self.X_test, batch_size=self.batch_size)).round()

        tn, fp, fn, tp = confusion_matrix(np.argmax(self.y_test, axis=1), np.argmax(predictions, axis=1)).ravel()
        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        
        print("----------------------------")

        print("Results for: ", self.name)
        print("TP: ", tp)
        print("FP: ", fp)
        print("TN: ", tn)
        print("FN: ", fn)
        # print("Sum of positives: ", tp+fn)
        # print("Sum of negatives: ", tn+fp)
        # print("Sum of all: ", tp+fp+tn+fn)

        print("Accuracy is: ", values[1])
        print('False positive rate is: ', fp / (fp + tn))
        print('False negative rate: ', fn / (fn + tp))
        print('True positive rate: ', recall)
        print('Precision: ', precision)
        print('F1 score: ', (2 * precision * recall) / (precision + recall))

        print("----------------------------")
