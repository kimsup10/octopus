from operator import attrgetter


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
        self.total_user_cnt = max(map(attrgetter('likes_count'), articles))
        for article in articles:
            for token in article.tokens:
                prob = article.likes_count / self.total_user_cnt
                if self.pre_prob.get(token, 0) < prob:
                    self.pre_prob[token] = prob

    def predict(self, article):
        '''키워드를 입력받아 좋아요 될 확률을 계산합니다

        return: 좋아할 확률 (0~1)
        rtype: float
        '''
        predicted_prob = 1.0
        count = 0
        for word in article.tokens:
            if self.pre_prob.get(word, 0) > 0:
                predicted_prob *= self.pre_prob[word]
                count += 1

        if count == 0:
            return 0

        return predicted_prob ** (1.0/count) * self.total_user_cnt
