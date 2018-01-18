#import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.classify import apply_features
from nltk.classify import accuracy
from nltk.corpus import stopwords
from Preproccessing import preprocess
import csv
from nltk import FreqDist
from nltk import ConfusionMatrix
import random
from Preproccessing import extract


def filter_tweets(tweets):

    """
    Preprocess and filter stop words from tweet text

    :param tweets extracted from file with sentiment:
            ex [('I do not like this car', 'negative'),('This view is horrible', 'negative')]
    :return: filtered text and its sentiment
            ex: [(['I', 'like', 'car'], 'negative'), (['This', 'view', 'horrible'], 'negative')]
    """
    filtered_tweets = []
    for (text, sentiment) in tweets:
        preprocessed_text = preprocess(text)
        words_filtered = [word for word in preprocessed_text if word not in stopwords.words("english")]
        filtered_tweets.append((words_filtered, sentiment))
    return filtered_tweets
"""
tweets = [('I do not like this car', 'negative'),
            ('This view is horrible', 'negative'),
            ('I feel tired this morning', 'negative'),
            ('I am not looking forward to the concert', 'negative'),
            ('He is my enemy', 'negative'),
            ('I love this car', 'positive'),
            ('This view is amazing', 'positive'),
            ('I feel great this morning', 'positive'),
            ('I am so excited about the concert', 'positive'),
            ('He is my best friend', 'positive')]"""

#print(filter_tweets([('I do not like this car', 'negative'),('This view is horrible', 'negative')]))

def get_words_in_tweets(tweets):
    """
    Donne la liste des mots contenus dans une liste labelisée de tweets
    Input:  liste de tweets labelisés
            exemple:    [('Wonder is an amazing movie','positive'),('This is a horrible movie','negative')]
    Output: Liste des mots contenus dans la liste sans les stopwords
            Exemple:    ['Wonder', 'amazing', 'movie', 'horrible', 'movie']
    """
    filtered = filter_tweets(tweets)
    all_words = []
    for (words, sentiment) in filtered:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    """
    Ordonne la liste de mots selon leur frequence
    Input:  liste de mots
            exemple:    [('Wonder is an amazing movie','positive'),('This is a horrible movie','negative')]
    Output: Liste des mots ordonnés
            Exemple:    ['Wonder', 'amazing', 'movie', 'horrible', 'movie']
    """
    wordlist = FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

print("Extracting tweets")
tweets = extract('Datasets/train2.tsv')
nr_tweets=len(tweets)

print("Getting featuress")
word_features = get_word_features(get_words_in_tweets(tweets))
# Enlever les duplications
featuresList = list(set(word_features))

def extract_features(document):
    """
    indiquer quels mots sont contenus dans l'entrée passée
    Input:  phrase
            Exemple: "I love this movie"
    Output: Dictionnaire
            Exemple:    {'contains(not)': False,
                        'contains(movie)': True,
                        'contains(best)': False,
                        'contains(excited)': False,
                        'contains(love)': True,
                        'contains(about)': False,
                        'contains(horrible)': False,
                        'contains(like)': False,
                        'contains(this)': True}

    """
    document_words = set(document.split())
    features = {}
    for word in featuresList:
        features['contains(%s)' % word] = (word in document_words)
    #print(features)
    return features

random.shuffle(tweets)

v_train = tweets[:2000]
v_test = tweets[:2000]


print("Training...")
training_set = apply_features(extract_features, v_train)
classifier = NaiveBayesClassifier.train(training_set)


tweet = "this movie is sweet and astonishing"
print(classifier.classify(extract_features(tweet)))

#print(classifier.show_most_informative_features(32))

print("Test...")
test_set = apply_features(extract_features, v_test)
print ('\nAccuracy %f\n' % accuracy(classifier, test_set))

# build confusion matrix over test set
test_truth = [s for (t, s) in v_test]
test_predict = [classifier.classify(t) for (t, s) in test_set]

print('Confusion Matrix')
print(ConfusionMatrix(test_truth, test_predict))

print("FIN")

