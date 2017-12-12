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


def analyse_doc(tweetsList):
    with open(tweetsList, 'r') as raw_data:
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




