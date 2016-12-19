#!/usr/bin/env python2
# -*- coding: utf-8; -*-

import random

from twitterbot import TwitterBot


class ParkerBot(TwitterBot):
    def hella_cred(self):
        with open('config') as fh:
            self.config['api_key'] = fh.readline().strip()
            self.config['api_secret'] = fh.readline().strip()
            self.config['access_key'] = fh.readline().strip()
            self.config[n'access_secret'] = fh.readline().strip()

    def bot_init(self):
        self.hella_cred()

        # how often to tweet, in seconds
        self.config['tweet_interval'] = 30 * 60     # default: 30 minutes
        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = None
        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False
        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = False
        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = True
        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []
        # follow back all followers?
        self.config['autofollow'] = True

        self.state['last_fav_search_id'] = 0
        self.phrases_to_fav = [
            '"@xor parker"',
        ]

        self.register_custom_handler(self.do_favs, 15 * 60 * 60)

    def on_scheduled_tweet(self):
        pass

    def on_mention(self, tweet, prefix):
        if (tweet.text.contains("parkerbot") or
            tweet.text.contains("parkertron9000")):
            self.post_tweet(prefix + " " + tweet.author.strip("@"))
        elif tweet.text.endswith("!"):
            self.post_tweet(prefix + " parker!", reply_to=tweet)
        else:
            self.post_tweet(prefix + " parker", reply_to=tweet)


    def make_attribution(self, tweet, prefix):
        d20 = random.randint(1, 20)
        if d20 in range(1, 6):
            self.post_tweet(prefix + " peak parker", reply_to=tweet)
        elif d20 in range(6, 11):
            self.post_tweet(prefix + " classic parker", reply_to=tweet)
        elif d20 in range(11, 16):
            self.post_tweet(prefix + " doesn't get more parker", reply_to=tweet)
        elif d20 in range(16, 21):
            self.post_tweet(prefix + " hoth couture parker", reply_to=tweet, media="hoth-couture.jpg")
            ##      ↑↑ MAX ROLL == HOTH COUTURE!!! ↑↑     ##

    def do_favs(self):
        for phrase in self.phrases_to_fav:
            results = self.api.search(phrase, since_id=self.state['last_fav_search_id'])

            self.state['last_fav_search_id'] = results.max_id

            for status in results:
                lower = status.text.lower()
                if phrase in lower.replace("#", "").replace("@", ""):
                    try:
                        status.favorite()
                    except tweepy.error.TweepError as exc:
                        self._log_tweepy_error('Error favoriting: ', exc)
                if lower == phrase:
                    try:
                        status.retweet()
                    except tweepy.error.TweepError as exc:
                        self._log_tweepy_error('Error retweeting: ', exc)


    def on_timeline(self, tweet, prefix):
        self.on_parkers_tweet(tweet, prefix)

    def on_parkers_tweet(self, tweet, prefix):
        if tweet.author.screen_name == "xor":
            self.post_tweet('@xor parker', reply_to=tweet)


if __name__ == '__main__':
    bot = ParkerBot()
    bot.run()
