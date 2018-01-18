import json
from Preproccessing import preprocess
import csv
from nltk import ConfusionMatrix
from Preproccessing import extract

def match_word(word,document):
    """
    Dans cette fonction on cherche le mot 'word' dans le document 'document'

    Input:
    ------
            :param word: mot recherché
            :param document: document où on cherche le mot

    Output:
    -------
            True: si le mot recherché est trouvé
            False: sinon

    :return:
    """

    with open(document,'r') as doc:
        for line in doc:
            if line[:1] != ';' and word == line[:-1]:
                return True
    return False


def positive_score(token):

    """

    :param token: text tokenisé d'un tweet
    :return:
    """

    pos_score = 0
    for elt in token:
        if match_word(elt,"Dictionary/positive-words.txt"):
            pos_score+=1
    return pos_score

def negative_score(token):
    neg_score = 0
    for elt in token:
        if match_word(elt,"Dictionary/negative-words.txt"):
            neg_score += 1
    return neg_score


def sentiment(token):
    tweet_sentiment = '1'
    neg = negative_score(token)
    pos = positive_score(token)
    total = pos-neg
    if total < 0:
        tweet_sentiment = '0'
    if total > 0:
        tweet_sentiment = '2'
    return tweet_sentiment

def analyse_data():
    with open('Datasets/train2.tsv','r') as data_in, open('Results/dictionary_train.tsv', 'w', newline='') as data_out:
        tsvin = csv.reader(data_in, delimiter='\t')
        tsvout = csv.writer(data_out, delimiter='\t')
        for row in tsvin:
            tweet = row[1]
                #print(tweet)
            token = preprocess(tweet)
                #print(token)
            tweet_sentiment = sentiment(token)
                #print(tweet_sentiment)
            print(tweet+' '+tweet_sentiment)
            tsvout.writerow((row[0], row[1], tweet_sentiment))


#analyse_data()

real_data = extract('Datasets/train2.tsv')
analysed_data = extract('Results/dictionary_train.tsv')
print(real_data)
print(analysed_data)
# build confusion matrix over test set
test_truth = [s for (t, s) in real_data]
test_predict = [s for (t, s) in analysed_data]
print('Confusion Matrix')
print(ConfusionMatrix(test_truth, test_predict))



