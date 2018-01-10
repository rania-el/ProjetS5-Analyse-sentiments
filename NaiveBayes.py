#import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.classify import apply_features
from nltk.corpus import stopwords
from Preproccessing import preprocess
import csv
from nltk import FreqDist


def extract(document):
    tweets=[]
    i=1
    with open(document, 'r') as data_in:
        data_in = csv.reader(data_in, delimiter='\t')
        for row in data_in:
            print(i)
            if row[1] == str(i):
                tweets.append((row[2], row[3]))
                i = i+1

    with open('tweet.txt', 'w') as ff:
        ff.write(str(tweets))
    return tweets


tweets = extract('Datasets/train.tsv')
print(tweets)


def filter_tweets(tweets):

    """
    Filter stop words from tweet text

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
        #print(filtered_tweets)
    return filtered_tweets

"""tweets = [('I do not like this car', 'negative'),
            ('This view is horrible', 'negative'),
            ('I feel tired this morning', 'negative'),
            ('I am not looking forward to the concert', 'negative'),
            ('He is my enemy', 'negative'),
            ('I love this car', 'positive'),
            ('This view is amazing', 'positive'),
            ('I feel great this morning', 'positive'),
            ('I am so excited about the concert', 'positive'),
            ('He is my best friend', 'positive')]"""

#print(filter_tweets(tweets))

def get_words_in_tweets(tweets):
    filtered=filter_tweets(tweets)
    all_words = []
    for (words, sentiment) in filtered:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


word_features = get_word_features(get_words_in_tweets(tweets))
print(word_features)

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = apply_features(extract_features, tweets)
print(training_set)

classifier = NaiveBayesClassifier.train(training_set)

print(classifier.show_most_informative_features(32))

