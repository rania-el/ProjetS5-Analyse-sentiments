import json

import nltk
import re
import regexes as regexes
from nltk import pos_tag
import string
import csv

def remove_urls(txt):
    """
    Input
    -----
        - a string
    Output
    ------
        - a cleaned string
    """
    tokens = txt.split(' ')
    clean_string = ''
    for token in tokens:
        match = re.search(regexes.URL_REGEX,token)
        if not match:
            clean_string += token + ' '

    return clean_string

def remove_punctuation(sentence):
    for c in string.punctuation:
        sentence = sentence.replace(c, "")
    return sentence

#print(remove_punctuation("ih . fsd. dze, ff! ?g"))

def remove_tweet_specific_chars(tokens):
    """
    Input
    -----
        - list of tokens
    Output
    ------
        - list of cleaned tokens
    """

    return [token for token in tokens if token != '@' and token != '#' and token != 'RT']


def preprocess(tweet):
    """
    Input
    -----
        - tweet : a string of words
            example 'I like this movie!!'
    Output
    ------
        - preProcessedTweet = list tokenized words
            example: ['I','like','this','movie']
    Algorithm
    ---------
        1. Remove urls
        2. Remove punctuation
        3. Tokenize the text
        4. Clean tweet specific characters (@ , # , RT)
    """

    tweet_url_cleaned = remove_urls(tweet) # 1. Remove urls
    tweet_no_punct = remove_punctuation(tweet_url_cleaned) # 2. Remove punctuation
    tokens = nltk.word_tokenize(tweet_no_punct) # 3. Tokenize the text
    tokens = remove_tweet_specific_chars(tokens) # 4 remove tweet specific chars
    return tokens


#print(preprocess("i love , how this ,: lfofdo ,dof."))

def extract(document):
    """
    Extraire les tweets depuis le data set avec leur sentiment correspondant
    Input:  dataset
            exemple:    12 2 this car is amazing 2
                        13 3 This is a horrible movie 0
    Output: Liste de tweets labelisés sous forme de dictionnaire
            exemple:    [('this car is amazing','positive'),('This is a horrible movie','negative')]
    """
    tweets = []
    i = 1

    with open(document, 'r') as data_in:
        data_in = csv.reader(data_in, delimiter='\t')
        for row in data_in:
            if row[2] == '0':
                sentiment = 'negative'
            elif row[2] == '2':
                sentiment = 'positive'
            else:
                sentiment = 'neutral'
            tweets.append((row[1], sentiment))
    return tweets