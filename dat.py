from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sqlite3
import json
import sentiment_mod as s


conn = sqlite3.connect('Donald.sqlite')
cur = conn.cursor()
script = '''
Drop table if exists tweets;
create table tweets (
    id Text Not Null PRIMARY KEY Unique,
    user_id Text Not Null,
    user_name Text Not Null,
    user_screen_name Text Not Null,
    user_loc Text,
    followers_count Integer Not Null,
    friends_count Integer Not Null,
    favourites_count Integer Not Null,
    statuses_count Integer Not Null,
    geo_enabled Text Not Null,
    user_lang Text Not Null,
    geo Text Not Null,
    coordinates Text Not Null,
    lang Text Not Null,
    retweeted_id Text,
    retweeted_created_at Text,
    retweeted_text Text,
    retweeted_user_id Text,
    retweeted_user_name Text,
    retweeted_user_location Text,
    entities Text Not Null,
    created_at Text Not Null,
    tweet_text Text Not Null,
    in_reply_to_status_id Text,
    in_reply_to_user_id Text,
    sentiment_value Float
);
'''
cur.executescript(script)


#Twitter API credentials
consumer_key = "yev654S6IjEqT1llVwamETvvj"
consumer_secret = "oWhhTko4qpjrFR0X4lBcfd1cIxeSbhDRyoXdU3y697g3UvLPrg"
access_token = "349555866-5DEzm7PJvEtSVCEFkojjs2M8ucDMVhq3UZdonjHT"
access_token_secret = "l3hCINaclx0pFSoHwwrBgpHpRTOm4CnrpVvfiVS1lSPsb"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        tweet=data["text"]
        sentiment_value,confidence = s.sentiment(tweet)


        #print(str(data)

        in_reply_to_status_id_str = ' '
        in_reply_to_user_id_str = ' '

        if(str(data['in_reply_to_status_id_str']) is not False):
            in_reply_to_status_id_str = str(data['in_reply_to_status_id_str'])
        else:
            in_reply_to_status_id_str = 'false'

        if(str(data['in_reply_to_user_id_str']) is not False):
            in_reply_to_user_id_str = str(data['in_reply_to_user_id_str'])
        else:
            in_reply_to_user_id_str = 'false'

        if('retweeted_status' in data.keys() and (data['retweeted_status'] is not False)):
            cur.execute('''Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?,?)''',
                          (str(data['id']), str(data['user']['id']), str(data['user']['name']), str(data['user']['screen_name']),
                           str(data['user']['location']),
                          str(data['user']['followers_count']), str(data['user']['friends_count']),
                          str(data['user']['favourites_count']),
                          str(data['user']['statuses_count']), str(data['user']['geo_enabled']), str(data['user']['lang']),
                          str(data['geo']),
                          str(data['coordinates']), str(data['lang']), str(data['retweeted_status']['id']),
                          str(data['retweeted_status']['created_at']),
                          str(data['retweeted_status']['text']), str(data['retweeted_status']['user']['id']),
                          str(data['retweeted_status']['user']['name']),
                          str(data['retweeted_status']['user']['location']), str(data['entities']), str(data['created_at']),
                          str(data['text']), in_reply_to_status_id_str, in_reply_to_user_id_str,sentiment_value))
            conn.commit()
        else:
            cur.execute('''Insert or Ignore into tweets values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?,?)''',
                          (str(data['id']), str(data['user']['id']), str(data['user']['name']), str(data['user']['screen_name']),
                           str(data['user']['location']),
                          str(data['user']['followers_count']), str(data['user']['friends_count']), str(data['user']['favourites_count']),
                          str(data['user']['statuses_count']), str(data['user']['geo_enabled']), str(data['user']['lang']), str(data['geo']),
                          str(data['coordinates']), str(data['lang']), 'false', 'false',
                          'false', 'false', 'false',
                          'false', str(data['entities']), str(data['created_at']),
                          str(data['text']),
                           in_reply_to_status_id_str,
                           in_reply_to_user_id_str,sentiment_value))
            conn.commit()

        cur.execute('select tweet_text from tweets where id = ?', (str(data['id']),))
        print(cur.fetchone())
        #print(type(str(data))


        #print(str(str(data['retweeted'])['id'])))
        return True
        

    def on_error(self, status):
        print (status)





if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture str(data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Donald Trump'])
