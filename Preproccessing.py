import json

import nltk
import re
import regexes as regexes
from nltk import pos_tag


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
            example 'I like this movie'
    Output
    ------
        - preProcessedTweet = list tokenized words
            example: ['I','like','this','movie']
    Algorithm
    ---------
        1. Retrieve text
        2. Tokenize the text
        3. Remove urls
        4. Clean tweet specific characters
        5. tag each token
    """

    tweet_url_cleaned = remove_urls(tweet) # 3. Remove urls
    tokens = nltk.word_tokenize(tweet_url_cleaned) # 2. Tokenize the text
    tokens = remove_tweet_specific_chars(tokens)
    #tagged_token=pos_tag(tokens)
    return  tokens


"""from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize


def tokenize(tweetslist):

    #Input:
     #   Json document where tweets are stocked
    #Output:

    with open(tweetslist, 'r') as doc:
        for line in doc:
            if line != '\n':
                tweet = json.loads(line)
                tweet = tweet["text"]
                token = preprocess(tweet)
                print(token)


def splitTweets(document):
    with open(document, 'r') as doc:
        for line in doc:
            if line != '\n':
                tweet = json.loads(line)
                tweet = tweet["text"]
                #token = clean_text(tweet)
                token = word_tokenize(tweet)
                print(token)

splitTweets('tweets.json')"""