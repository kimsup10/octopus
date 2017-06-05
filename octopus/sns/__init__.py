from functools import reduce
from operator import attrgetter
from .. import config
from .instagram import InstagramAPI

api = InstagramAPI(config['instagram']['username'],
                   config['instagram']['password'])


def get_articles(target_page_id=None, limit=None):
    '''인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :param limit: 갯수 제한
    :return: list of `octopus.instagram.InstagramArticle`
    :rtype: list
    '''
    if limit is None:
        limit = 100
    return api.get_articles(target_page_id)[:limit]


def get_user_likes_map(target_page_id=None, limit=None):
    '''인사타그램 유저-좋아요벡터맵을 가져옵니다 (클러스터링용)

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :return: {'follwer1':[True, False, ....], ...}
    :rtype: dict
    '''
    articles = get_articles(target_page_id, limit)
    users = sorted(reduce(set.union, map(attrgetter('engaged_users'),
                                         articles)))
    return {user: [user in article.engaged_users for article in articles]
            for user in users}
