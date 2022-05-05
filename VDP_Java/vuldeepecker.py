"""
Interface to VulDeePecker project
"""
import sys
import os
import pandas
from clean_gadget import clean_gadget
from vectorize_gadget import GadgetVectorizer
from blstm import BLSTM
from tensorflow.keras.callbacks import TensorBoard
import time

"""
Parses gadget file to find individual gadgets
Yields each gadget as list of strings, where each element is code line
Has to ignore first line of each gadget, which starts as integer+space
At the end of each code gadget is binary value
    This indicates whether or not there is vulnerability in that gadget
"""

def parse_file(filename):
    with open(filename, "r", encoding="utf8") as file:
        gadget = []
        gadget_val = 0
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue
            if "-" * 33 in line and gadget: 
                yield clean_gadget(gadget), gadget_val
                gadget = []
            elif stripped.split()[0].isdigit():
                if gadget:
                    # Code line could start with number (somehow)
                    if stripped.isdigit():
                        gadget_val = int(stripped)
                    else:
                        gadget.append(stripped)
            else:
                gadget.append(stripped)

"""
Uses gadget file parser to get gadgets and vulnerability indicators
Assuming all gadgets can fit in memory, build list of gadget dictionaries
    Dictionary contains gadgets and vulnerability indicator
    Add each gadget to GadgetVectorizer
Train GadgetVectorizer model, prepare for vectorization
Loop again through list of gadgets
    Vectorize each gadget and put vector into new list
Convert list of dictionaries to dataframe when all gadgets are processed
"""
def get_vectors_df(filename, vector_length=100):
    gadgets = []
    count = 0
    vectorizer = GadgetVectorizer(vector_length)
    for gadget, val in parse_file(filename):
        count += 1
        print("Collecting gadgets...", count, end="\r")
        vectorizer.add_gadget(gadget)
        row = {"gadget" : gadget, "val" : val}
        gadgets.append(row)
    print('Found {} slices'
          .format(vectorizer.forward_slices + vectorizer.backward_slices))
    print()
    print("Training model...", end="\r")
    vectorizer.train_model()
    print()
    vectors = []
    count = 0
    for gadget in gadgets:
        count += 1
        print("Processing gadgets...", count, end="\r")
        vector = vectorizer.vectorize(gadget["gadget"])
        row = {"vector" : vector, "val" : gadget["val"]}
        vectors.append(row)
    print()
    df = pandas.DataFrame(vectors)
    return df
            
"""
Gets filename, either loads vector DataFrame if exists or creates it if not
Instantiate neural network, pass data to it, train, test, print accuracy
"""
def main():
    if len(sys.argv) != 2:
        print("Usage: python vuldeepecker.py [filename]")
        exit()
    filename = sys.argv[1]
    parse_file(filename)
    base = os.path.splitext(os.path.basename(filename))[0]
    vector_filename = base + "_gadget_vectors.pkl"
    vector_length = 100
    if os.path.exists(vector_filename):
        df = pandas.read_pickle(vector_filename)
    else:
        df = get_vectors_df(filename, vector_length)
        df.to_pickle(vector_filename)


    # Running multiple configurations
    # layers = [1, 2, 3, 4]
    # resamplings = [0.75, 1.0]
    # reweightings = [True, False]
    # losses = ['binary_crossentropy', 'categorical_crossentropy']

    # Running a specific configuration
    layers = [3]
    resamplings = [1.0]
    reweightings = [False]
    losses = ['binary_crossentropy']

    i = 0

    for layer in layers:
        for resampling in resamplings:
            for loss in losses:
                for reweighting in reweightings:

                    i+=1

                    # Modify to only run a subset of models
                    if i >0:
    
                        NAME = "{}-{}_{}_{}_{}_{}".format(base, layer, resampling, loss, reweighting, int(time.time()))
        
                        print("*********** Beginning: training and testing ************")
                        print("Running: ", NAME, " - [", i, "]")
        
                        blstm = BLSTM(df, resampling, 1, reweighting, layer, loss, NAME)
                        blstm.train()
                        blstm.test()
        
                        print("************ End: training and testing ***********")

if __name__ == "__main__":
    main()
