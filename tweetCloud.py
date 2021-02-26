#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py
import csv

import tweepy
import logging
from config import create_api
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        sn = tweet.user.screen_name
        if tweet.in_reply_to_status_id is not None:
            continue


        if not tweet.user.following:
            tweet.user.follow()
        m = f'@{tweet.author.screen_name} Here is your word cloud'
        # api.update_status(
        #     m,
        #     in_reply_to_status_id=tweet.id,
        #     auto_populate_reply_metadata=True
        # )
        get_all_tweets(api, sn)
        make_cloud(f'{sn}_tweets.txt',sn)
        pic = api.media_upload(f'{sn}_cloud.png')
        api.update_status(m, media_ids=[pic.media_id_string],
                          in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    return new_since_id
#####################################################################
def get_all_tweets(api,screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

    # write the csv
    with open(f'{screen_name}_tweets.csv', 'w',  encoding='utf-8') as f:
        writer = csv.writer(f)
        # #writer.writerow(["id", "created_at", "text"])
        # writer.writerow(["text"])
        writer.writerows(outtweets)
    csv_file = f'{screen_name}_tweets.csv'
    txt_file = f'{screen_name}_tweets.txt'
    with open(txt_file, "w",encoding='utf-8') as my_output_file:
        with open(csv_file, "r", encoding='utf-8') as my_input_file:
            [my_output_file.write(" ".join(row) + '\n') for row in csv.reader(my_input_file)]
        my_output_file.close()


    pass


def make_cloud(in_file, sn):
    # Load a text file as a string.
    with open(in_file, encoding='utf-8') as infile:
        text = infile.read()

    # Load an image as a NumPy array.
    mask = np.array(Image.open('rec.png'))

    # Get stop words as a set and add extra words.
    stopwords = STOPWORDS
    stopwords.update(['RT', 'https', 'co', 's','a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','t','u','v','w','x','y','z'])

    # Generate word cloud.
    wc = WordCloud(max_words=500,
                   relative_scaling=0.5,
                   mask=mask,
                   background_color='black',
                   stopwords=stopwords,
                   margin=2,
                   random_state=7,
                   contour_width=2,
                   contour_color='black',
                   colormap='Set2').generate(text)

    # Turn wc object into an array.
    colors = wc.to_array()

    # Plot and save word cloud.
    plt.figure()
    plt.title(f"{sn}:\n",
              fontsize=15, color='black')
    # plt.suptitle("7:00 pm May 10-12 McComb Auditorium",
    #              x=0.52, y=0.095, fontsize=15, color='brown')
    plt.imshow(colors, interpolation="bilinear")
    plt.axis('off')
    #plt.show()
    plt.savefig(f'{sn}_cloud.png')

#####################################################################


def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
