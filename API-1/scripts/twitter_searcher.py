#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import time
from utils import open_csv_w

# import authentication credentials
from secrets import TWITTER_C_KEY, TWITTER_C_SECRET, TWITTER_A_KEY, TWITTER_A_SECRET

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_C_KEY, TWITTER_C_SECRET)
auth.set_access_token(TWITTER_A_KEY, TWITTER_A_SECRET)
api = tweepy.API(auth)

# Twitter API limit handler; this helps you deal with the fact that Twitter only allows you to ping its API a set number of times
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.error.TweepError:
            print("waiting 15 minutes for Twitter to let me get more tweets")
            time.sleep(15 * 60)

# counter for console messages
counter  = 0;

# search terms
# find a full list of conventions here: https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators
searchterm = "#MuellerReport"

# Open/Create a file to append data
csvFile = open_csv_w('../output/%s-result.csv' % searchterm)
#Use csv Writer
csvWriter = csv.writer(csvFile)
# these are the headers of your csv
csvWriter.writerow(["id",
				"created_at",
				"favorites",
				"retweets",
				"retweeted",
				"source",
				"text",
				"geolocation",
				"language",
				"is_quote_status",
				"username",
				"user_screen_name",
				"user_location",
				"user_description",
				"user_protected",
				"user_followers_count",
				"user_friends_count",
				"user_listed_count",
				"user_created_at",
				"user_favourites_count",
				"user_utc_offset",
				"user_time_zone",
				"user_geo_enabled",
				"user_verified",
				"user_statuses_count",
				"user_lang"])

# loop to put tweets into the csv
for tweet in limit_handled(tweepy.Cursor(api.search,
                    q=searchterm,
                    # note that Twitter only makes available a sample of tweets from the last 7 days: https://dev.twitter.com/rest/public/search
                    # point of time you want the search to start
                    since="2019-01-10",
                    # point of time you want the search to end
                    until="2019-04-19",
                    lang="en").items()):
    #Write a row to the csv file/ I use encode utf-8
    csvWriter.writerow([tweet.id_str,
        				tweet.created_at,
        				tweet.favorite_count,
        				tweet.retweet_count,
        				tweet.retweeted,
        				tweet.source,
        				tweet.text,
        				tweet.geo,
        				tweet.lang,
        				tweet.is_quote_status,
        				tweet.user.name,
        				tweet.user.screen_name,
        				tweet.user.location,
        				tweet.user.description,
        				tweet.user.protected,
        				tweet.user.followers_count,
        				tweet.user.friends_count,
        				tweet.user.listed_count,
        				tweet.user.created_at,
        				tweet.user.favourites_count,
        				tweet.user.utc_offset,
        				tweet.user.time_zone,
        				tweet.user.geo_enabled,
        				tweet.user.verified,
        				tweet.user.statuses_count,
        				tweet.user.lang])
    # this code prints information in your console while you're getting tweets
    counter += 1
    if counter % 100 == 0:
        print("%s tweets collected" % counter)

# close the file
csvFile.close()
