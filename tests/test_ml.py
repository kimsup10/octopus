import logging
import numpy as np
from unittest import TestCase
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import KFold
from octopus.ml.naive_bayes import NaiveBayes
from octopus.ml.clustering import KMeansClustering, DunnIndexEvaluator
from octopus.sns import get_articles, get_user_likes_map


class ML(TestCase):
    def evaluate_nb(self, nb, X):
        y_true = list(map(lambda a: a.likes_count, X))
        y_pred = list(map(nb.predict, X))
        return r2_score(y_true, y_pred), mean_squared_error(y_true, y_pred)

    def test_naive_bayes(self):
        logger = logging.getLogger()
        articles = get_articles('felix_alterego')
        X = articles
        nb = NaiveBayes(X)
        r2, mse = self.evaluate_nb(nb, X)
        print('[No CV] R2: %r, MSE: %r' % (r2, mse))
        kf = KFold(10)
        train_result, test_result = [], []
        for i, (train, test) in enumerate(kf.split(articles), 1):
            X = np.array(articles)[train]
            nb = NaiveBayes(X)
            r2, mse = self.evaluate_nb(nb, X)
            train_result.append([r2, mse])
            logger.warning('[%dth CV Train] R2: %r, MSE: %r' % (i, r2, mse))

            X = np.array(articles)[test]
            r2, mse = self.evaluate_nb(nb, X)
            test_result.append([r2, mse])
            logger.warning('[%dth CV Test] R2 : %r, MSE: %r' % (i, r2, mse))
        mean_r2 = np.array(test_result)[:, :1].mean()
        mean_mse = np.array(test_result)[:, 1:].mean()
        print('[CV Mean] R2: %r, MSE: %r' % (mean_r2, mean_mse))
        self.assertGreater(mean_r2, 0.5)

    def test_clustering(self):
        logger = logging.getLogger()
        k = KMeansClustering(get_user_likes_map('yadoran_q'))
        for i, cluster in enumerate(k.cluster()):
            logger.warning('%dth Cluster: %r' % (i+1, cluster["users"]))

    def test_max_inter_distance(self):
        logger = logging.getLogger()
        k = KMeansClustering(get_user_likes_map('yadoran_q'))
        e = DunnIndexEvaluator()
        di = e.evaluate(k.cluster())
        logger.warning('DI: %d' % di)
        self.assertGreater(di, 0)
