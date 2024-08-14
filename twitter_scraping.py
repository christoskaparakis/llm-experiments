import asyncio
from twikit import Client
import time
import csv
from random import randint
import datetime as dt
from tqdm import tqdm


USERNAME = 'synaryth'
EMAIL = 'thyranys+synaryth@gmail.com'
PASSWORD = 'yF1yN@tw'

# Initialize client
client = Client('en-US')

# async def main():
#     await client.login(
#         auth_info_1=USERNAME ,
#         auth_info_2=EMAIL,
#         password=PASSWORD
#     )
#
# asyncio.run(main())
# client.save_cookies('cookies.json');

client.load_cookies(path='cookies.json');

async def main():
    tweets = []
    scraped_tweets = await client.search_tweet('@ingnl', 'Latest')
    tweets.extend(scraped_tweets)
    for i in tqdm(range(25)):
        time.sleep(randint(1, 25))
        scraped_tweets = await scraped_tweets.next()
        tweets.extend(scraped_tweets)
    return tweets

scraped_tweets = asyncio.run(main())

tweets = []
for tweet in scraped_tweets:
    if tweet.user.screen_name != "ingnl":
        tweets.append({
            "user_name": tweet.user.screen_name,
            "created at": tweet.created_at,
            "favorite_count": tweet.favorite_count,
            "text": tweet.text.replace('\n', ' '),
            "id": tweet.id,
            "in_reply_to": tweet.in_reply_to,
            "is_reply": tweet.in_reply_to is not None,
            "lang": tweet.lang,
            "view_count": int(tweet.view_count),
            "retweet_count": tweet.retweet_count
        })

keys = tweets[0].keys()

timenow = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d%H%M%S")

with open(f'tweets_{timenow}.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tweets)
