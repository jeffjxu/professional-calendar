import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
####################################################################

####################################################################
# Read in multiple JSON Files and preprocess files into pandas 
# dataframe. Does basic N/A removal.
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
            f = (df['description'] != 'n/a')
            df = df[f]
            df['category'] = i
            def label_category(row):
                if row['category'] == 1:
                    return 'business'
                if row['category'] == 2:
                    return 'design'
                if row['category'] == 3:
                    return 'engineering'
                if row['category'] == 4:
                    return 'general'
                if row['category'] == 5:
                    return 'events'
            df['category_id'] = df.apply(lambda row: label_category(row), axis = 1)
            frames.append(df)
    df = pd.concat(frames)
    # Shuffle Dataframe to remove bias.
    df = df.reindex(np.random.permutation(df.index))
    df = df[pd.notnull(df['description'])]
    return df
    
####################################################################
# Create Counts of special dataframe.
# REQUIRES - dataframe with category and description 
# ENSURES - Plot of counts
####################################################################
def plotCounts(df):
    fig = plt.figure(figsize = (8, 6))
    df.groupby('category_id').description.count().plot.bar(ylim = 0)
    plt.show()

def wordAssociation(df, tfidf, features, labels):
    category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category')
    category_to_id = dict(category_id_df.values)
    N = 2
    for cat_id, category in sorted(category_to_id.items()):
        features_chi2 = chi2(features, labels == cat_id)
        idx = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[idx]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        trigrams = [v for v in feature_names if len(v.split(' ')) == 3]
        print("# '{}':".format(category))
        print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
        print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))
        print("  . Most correlated trigrams:\n       . {}".format('\n       . '.join(trigrams[-N:])))

def main():
    trainingSet = preprocessText()
    # plotCounts(trainingSet)
    tfidf = TfidfVectorizer(sublinear_tf = True, min_df = 8, norm = 'l2',
                            encoding = 'latin-1', ngram_range= (1, 3), stop_words = 'english')
    features = tfidf.fit_transform(trainingSet.description).toarray()
    labels = trainingSet.category
    wordAssociation(trainingSet, tfidf, features, labels)



    

if __name__ == "__main__":
    main()