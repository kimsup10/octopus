import logging
from unittest import TestCase
from octopus.sns import get_articles, get_user_likes_map
from octopus.sns.article import InstagramArticle


class SNS(TestCase):
    def test_get_articles(self):
        articles = get_articles('yadoran_q')
        logging.getLogger().warning(articles)
        self.assertIsInstance(articles[0], InstagramArticle)

    def test_user_likes_map(self):
        r = get_user_likes_map('yadoran_q')
        logging.getLogger().warning(r)
        self.assertIsInstance(r, dict)
