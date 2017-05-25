import logging
from unittest import TestCase
from octopus.ml.naive_bayes import NaiveBayes
from octopus.sns import get_articles


class ML(TestCase):
    def test_naive_bayes(self):
        nb = NaiveBayes(get_articles('yadoran_q'))
        test_cases = [
            (['일본', '한국'], 1),
            (['연어회'], 3),
        ]
        logger = logging.getLogger()
        for case, Y in test_cases:
            probability = nb.predict(case)
            predicted_likes_cnt = nb.total_user_cnt * probability
            logger.warning('Case: %r' % case)
            logger.warning("NB Prob.: %.2f" % probability)
            logger.warning("NB Cnt.: %d" % predicted_likes_cnt)
            self.assertEqual(predicted_likes_cnt, Y)
