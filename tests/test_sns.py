import logging, json
import requests
from unittest import TestCase
from octopus.sns import get_articles, get_user_likes_map
from octopus.sns.article import InstagramArticle


class SNS(TestCase):
    def test_get_articles(self):
        username = "kimsup10"
        url = "https://www.instagram.com/"+username+"/?__a=1"
        res = requests.get(url)
        user_id = json.loads(res.content.decode('utf-8'))["user"]["id"]

        articles = get_articles(user_id)
        self.assertIsInstance(articles[0], InstagramArticle)

    def test_user_likes_map(self):
        r = get_user_likes_map('huntrax11')
        logging.getLogger().warning(r)
        self.assertIsInstance(r, dict)
