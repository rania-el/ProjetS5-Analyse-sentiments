import json
from Preproccessing import preprocess

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

    pos_score=0
    for elt in token:
        if match_word(elt,"Dictionary/positive-words.txt"):
            pos_score+=1
    return pos_score

def negative_score(token):
    neg_score=0
    for elt in token:
        if match_word(elt,"Dictionary/negative-words.txt"):
            neg_score+=1
    return neg_score


def sentiment(token):
    tweet_sentiment = 'neutral'
    neg = negative_score(token)
    pos = positive_score(token)
    total = pos-neg
    if total < 0:
        tweet_sentiment = 'negative'
    if total > 0:
        tweet_sentiment = 'positive'
    return tweet_sentiment



"""
def analyse_extracted_doc(jsondoc):
    with open(jsondoc, 'r') as raw_data:
        with open('Results/resultsDictionary.json', 'w') as result:
            for line in raw_data:
                if line != '\n':
                    tweet = json.loads(line)
                    tweet = tweet["text"]
                    #print (tweet)
                    token = preprocess(tweet)
                    #print(token)
                    tweet_sentiment = sentiment(token)
                    #print(tweet_sentiment)
                    json.dump({'tweet': tweet, 'sentiment': tweet_sentiment}, result)

    print("SUCCESS")
"""

def analyse_test_data():
    with open('Datasets/train.tsv','r') as data_in, open('Results/dictionary_train.tsv', 'w', newline='') as data_out:
        tsvin = csv.reader(data_in, delimiter='\t')
        tsvout = csv.writer(data_out,delimiter='\t')

        for row in tsvin:
            tweet = row[2]
            token = preprocess(tweet)
            tweet_sentiment = sentiment(token)
            print(tweet+' '+tweet_sentiment)
            tsvout.writerow((row[0], row[1], row[2], tweet_sentiment))


analyse_test_data()

def compare():
    with open('Datasets/train2.tsv','r') as real_data, open('Results/dictionary_train.tsv', 'r') as analysed_data:
        real_data = csv.reader(real_data, delimiter='\t')
        analysed_data = csv.reader(analysed_data, delimiter='\t')
        total=0
        differences=0
        for real, analysed in itertools.izip(real_data, analysed_data):
            total+=1
            if real[3]!=analysed[3]:
                print ("difference")
                differences+=1

    print(str(differences) + " differenes out of "+str(total))


