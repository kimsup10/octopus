import logging
import numpy as np
import pandas as pd
from unittest import TestCase
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import KFold
from octopus.ml.naive_bayes import NaiveBayes
from octopus.ml.clustering import KMeansClustering
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
        logger.warning('[Without CV]\nR2: %r, MSE: %r' % (r2, mse))

        np.random.seed(0)
        result = pd.DataFrame()
        kf = KFold(10, shuffle=True)
        for train, test in kf.split(articles):
            X = np.array(articles)[train]
            nb = NaiveBayes(X)
            r2_train, mse_train = self.evaluate_nb(nb, X)
            X = np.array(articles)[test]
            r2_test, mse_test = self.evaluate_nb(nb, X)
            result = result.append(pd.DataFrame(
                [[r2_train, mse_train, r2_test, mse_test]],
                columns=["Train R2", "Train MSE", "Test R2", "Test MSE"]
            ))
        logger.warning('[10-Fold CV]\n%s' % result.describe())
        self.assertGreater(result['Test R2'].median(), 0.0)

    def test_clustering(self):
        logger = logging.getLogger()
        k = KMeansClustering(get_user_likes_map('felix_alterego'))
        for i, cluster in enumerate(k.cluster()):
            logger.warning('%dth Cluster: %r' % (i+1, cluster["users"]))
