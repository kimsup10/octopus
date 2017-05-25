from unittest import TestCase
from octopus.ml import setting
from octopus.ml import get_naive_bayes


class ML(TestCase):
    def test_naive_bayes(self):
        setting()
        get_naive_bayes()
