import sys, os, json
import pandas as pd
import numpy as np
import sklearn
####################################################################

####################################################################
# Read in multiple JSON Files and preprocess files into pandas 
# dataframe. Does not remove NULL, N/A.
# REQUIRES - JSON Files (each representing their own classifcation)
# ENSURES - Pandas Dataframe of Training Set
####################################################################
def preprocessText():
    frames = []
    # Depending on number of JSON Files Provided
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i]) as f:
            df = pd.read_json(f)
            df = df.transpose()
            col = ['name', 'description']
            df = df[col]
            df['category'] = i
            frames.append(df)
    df = pd.concat(frames)
    # Shuffle Dataframe to remove bias.
    df = df.reindex(np.random.permutation(df.index))
    return df
    

def main():
    trainingSet = preprocessText()

if __name__ == "__main__":
    main()