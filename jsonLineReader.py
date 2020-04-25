import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob

import re
class Json_reader():
    """
    this class inherits from json library
    """
    def dump_jsonl(self, data, output_path, append=False):
        """"
        Write list of objects to a JSON lines file.
        """
        mode = 'a+' if append else 'w'
        with open(output_path, mode, encoding='utf-8') as f:
            for line in data:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + '\n')
        print('Wrote {} records to {}'.format(len(data), output_path))

    def load_jsonl(self,input_path) -> list:
        """
        Read list of objects from a JSON lines file.
        """
        data = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.rstrip('\n|\r')))
        print('Loaded {} records from {}'.format(len(data), input_path))
        return data
class TweetAnalyser():
    """
    this class will analyse what is in the tweets
    """
    def clean_text(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", text).split())

    def sentiment_analyse(self, text):
        analysis = TextBlob(self.clean_text(text))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    def tweets_daframe_covert(self, tweets):
        df = pd.DataFrame(data=[tweet.get('full_text') for tweet in tweets], columns=['Tweet'])
        df['date'] = np.array([tweet.get('created_at') for tweet in tweets])
        df['language'] = np.array([tweet.get('lang') for tweet in tweets])
        df['likes'] = np.array([tweet.get('favorite_count') for tweet in tweets])
        df['RT'] = np.array([tweet.get('retweet_count') for tweet in tweets])
        #df['location'] = np.array([tweet.get('location') for tweet in tweets])
        return df

if __name__ == '__main__':
    tweet_dataset = Json_reader()
    tweet_analyser = TweetAnalyser()

    dataset = tweet_dataset.load_jsonl('tweets.jsonl')
    #print(dataset[0])
    df = tweet_analyser.tweets_daframe_covert(dataset)
    df['Sentiment'] = np.array([tweet_analyser.sentiment_analyse(tweet) for tweet in df['Tweet']])
    #jsonDataset = load_jsonl('tweets.jsonl')
    print(df)
    #for x in jsonDataset:
    #print(x.get('created_at'))
    time_likes = pd.Series(data=df['Sentiment'].values, index=df['date'])
    time_likes.plot(figsize=(200,10))
    plt.show()
    #pos = np.array([tweet_analyser.sentiment_analyse(tweet) for tweet in df['Tweet']])
    #neg
    #neu
