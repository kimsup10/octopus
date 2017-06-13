import numpy as np


class NaiveBayes:
    '''전체 유저수'''
    total_user_cnt = None

    '''사전확률'''
    pre_prob = None

    '''좋아요 수 평균'''
    mean_likes_cnt = None

    def __init__(self, articles):
        self.prepare(articles)

    def prepare(self, articles):
        '''나이브 베이즈 사전확률 계산'''
        self.pre_prob = {}
        likes_cnt = [a.likes_count for a in articles]
        self.total_user_cnt = np.max(likes_cnt)
        self.mean_likes_cnt = np.mean(likes_cnt)
        for article in articles:
            for token in article.tokens:
                prob = article.likes_count / self.total_user_cnt
                self.pre_prob.setdefault(token, []).append(prob)
        for k, v in self.pre_prob.items():
            self.pre_prob[k] = np.mean(v)

    def predict(self, article):
        '''Article의 예상 좋아요 수를 계산합니다

        return: 예상 좋아요수
        rtype: float
        '''
        predicted_prob = 1.0
        count = 0
        for word in article.tokens:
            if self.pre_prob.get(word, 0) > 0:
                predicted_prob *= self.pre_prob[word]
                count += 1

        if count == 0:
            return self.mean_likes_cnt

        return predicted_prob ** (1.0/count) * self.total_user_cnt
