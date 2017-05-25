from functools import reduce
from operator import attrgetter
from ..preprocessing import process


class NaiveBayes:
    '''전체 유저수'''
    total_user_cnt = None

    '''사전확률'''
    pre_prob = None

    def __init__(self, articles):
        self.prepare(articles)

    def prepare(self, articles):
        '''나이브 베이즈 사전확률 계산'''
        self.pre_prob = {}
        self.total_user_cnt = \
            len(reduce(set.union, map(attrgetter('liked_users'), articles)))
        for article in articles:
            for token in set(process(article.text)):
                prob = len(article.liked_users) / self.total_user_cnt
                if self.pre_prob.get(token, 0) < prob:
                    self.pre_prob[token] = prob

    def predict(self, words):
        '''키워드를 입력받아 좋아요 될 확률을 계산합니다

        return: 좋아할 확률 (0~1)
        rtype: float
        '''
        predicted_prob = 1.0
        count = 0
        for word in words:
            if self.pre_prob.get(word, 0) > 0:
                predicted_prob *= self.pre_prob[word]
                count += 1

        return predicted_prob ** (1.0/count)
