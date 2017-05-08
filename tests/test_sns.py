import logging
from unittest import TestCase
from octopus.sns import get_user_likes_map


class SNS(TestCase):
    def test_user_likes_map(self):
        r = get_user_likes_map('huntrax11')
        logging.getLogger().warning(r)
        self.assertIsInstance(r, dict)
