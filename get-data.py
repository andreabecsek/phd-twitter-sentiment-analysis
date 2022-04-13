import tweepy
import pandas as pd
import re
import nltk
import textblob

consumer_key = "WMNn14BNfae30vyhLrAWXYrFx"
consumer_secret = "3xZj71VSs8Ovyv3o5tBtYT8yM2Z4HAMauLfW5DOIMQIBE7qMsS"
access_token = "1316389508527673350-mN3rVU99jhyW6e6E1xBulzkqOJUV1e"
access_token_secret = "QUhEoHSf3Iz94n6nFp1ZLs3mA6BCcz7vsfA9jnhZGTeEs"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAOrIbQEAAAAAcUr8m%2BbWAcizcDhOVgMW9XJVfJA%3DZFK8ERAJnbyUQ5cDuCChsJXfKQbA7FpjAEnwwvtkeDBKo16lMM"


# # create api authentification object
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# # setting access token and secret
# auth.set_access_token(access_token, access_token_secret)
# # create api object
# api = tweepy.API(auth)

def getTweets(query, num_tweets=50):
    # connect to api
    client = tweepy.Client(bearer_token=bearer_token)

    # use tweepy paginator to get over 100 tweets
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets,
                                  query=query,
                                  tweet_fields=['id', 'created_at', 'public_metrics', 'text', 'source', 'context_annotations'],
                                  max_results=num_tweets,
                                  expansions=['geo.place_id']).flatten(limit=500):
        tweets.append(tweet)
    return tweets


# regex function to clean the tweet text from haashtags, mentions and links
def cleanTweets(text):
    clean_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    return clean_text


def tweetsToDF(tweets):
    data = []
    for tweet in tweets:
        data.append({'id': tweet.id,
                     'text': tweet.text,
                     'clean_tweet': cleanTweets(tweet.text),
                     'created_at': tweet.created_at,
                     'retweets': tweet.public_metrics['retweet_count'],
                     'replies': tweet.public_metrics['reply_count'],
                     'likes': tweet.public_metrics['like_count'],
                     'quote_count': tweet.public_metrics['quote_count'],
                     'sentiment': getTweetSentiment(tweet.text),
                     'location': tweet.geo.place_id

                     })
    df = pd.DataFrame(data)
    return df

def getTweetSentiment(tweet):
    # create text blob of tweet text
    analysis = textblob.TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


tweets = getTweets(query='phd')
tweetsDF = tweetsToDF(tweets)

