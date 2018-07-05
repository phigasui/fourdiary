#! /usr/local/bin/python3

import requests
from  requests_oauthlib import OAuth1
import json
import doc_anal
import certifications


api_key = certifications.API_KEY
api_secret = certifications.API_SECRET


def get_usertimeline(access_token, access_token_secret):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    params = {# 'q': word,
              # 'since_id': 530704728129556480,
              # 'max_id': 532722531099496448,
              'count': 200}


    res = requests.get(url, auth=auth, params=params)

    return json.loads(res.text)


def get_hometimeline(access_token, access_token_secret):
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    res = requests.get(url, auth=auth)

    return json.loads(res.text)


def search_tweets(access_token, access_token_secret, word):

    url = 'https://api.twitter.com/1.1/search/tweets.json'

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    params = {'q': word,
              # 'since_id': 530704728129556480,
              # 'max_id': 532722531099496448,
              'count': 100}

    res = requests.get(url, auth=auth, params=params)

    print(res)

    return json.loads(res.text)['statuses']


def streaming(access_token, access_token_secret):

    url = 'https://stream.twitter.com/1.1/statuses/sample.json'

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)

    res = requests.get(url, auth=auth)

    return json.loads(res.text)


# def oauth1request(url, access_token, access_token_secret, params={}):

#     keys = {'api_key': api_key,
#             'api_secret': api_secret,
#             'access_token': access_token,
#             'access_token_secret': access_token_secret}

#     encoded_keys = urllib.parse.urlencode(keys)
#     encoded_params = urllib.parse.urlencode(params)

#     res = urllib.request.urlopen(url + '?' + encoded_params, encoded_keys)

#     return res.read()


if __name__ == '__main__':

    access_token = certifications.ACCESS_TOKEN
    access_token_secret = certifications.ACCESS_TOKEN_SECRET

    data = get_usertimeline(access_token, access_token_secret)

    tweets = []
    tweets_without_link = []
    for tweet in data:

        if 'retweeted_status' in tweet: continue

        tweets.append(tweet['text'])

        text = tweet['text']
        for url in tweet['entities']['urls']:
            text = text.replace(url['url'], ' ')

        for mention in tweet['entities']['user_mentions']:
            text = text.replace('@' + mention['screen_name'], ' ')

        for tag in tweet['entities']['hashtags']:
            text = text.replace('#' + tag['text'], ' ' + tag['text'])

        tweets_without_link.append(text)

    print(tweets)
    print(tweets_without_link)

    print(json.dumps(doc_anal.extract_keywords(' '.join(tweets_without_link)),
                     ensure_ascii=False))


    # word = '飯テロ'

    # # print(streaming(access_token, access_token_secret))

    # for tweet in search_tweets(access_token, access_token_secret, word):
    #     if 'media' in tweet['entities']:
    #         for m in tweet['entities']['media']:
    #             if m['type'] == 'photo':
    #                 print(m)
