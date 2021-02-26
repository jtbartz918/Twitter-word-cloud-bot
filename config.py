# tweepy-bots/bots/config.py
import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    consumer_key = "2rAC5iOQ7YL1yovgDU4ln7Lz8"
    consumer_secret = "dc19J6QVe2AqHM5eGRQbNuGvoDhw2DL4CENFoMjFueLcAlf4BF"
    access_token = "1361647119078219776-xvKh9tIA0gJYNrjxy6UoyQodvBddi9"
    access_token_secret = "POyWltFmRzAwntFIinzPxrmcJ86ezrMY4dN8BAi1jq8cT"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api