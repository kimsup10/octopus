from functools import reduce, partial
from operator import attrgetter
from .article import InstagramArticle
from .instagram import InstagramAPI

api = InstagramAPI()


def get_articles(target_page_id=None, limit=None):
    '''인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :param limit: 갯수 제한
    :return: list of `octopus.instagram.InstagramArticle`
    :rtype: list
    '''
    if limit is None:
        limit = 100
    articles = api.get_recent_media(target_page_id)['data'][:limit]
    converter = partial(InstagramArticle.from_media, api)
    return list(map(converter, articles))


def get_dummy_articles(target_page_id, limit=None):
    '''가짜 인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID
    :param limit: 갯수 제한
    :return: list of `octopus.instagram.InstagramArticle`
    :rtype: list
    '''
    return [
        InstagramArticle(
            'Dummy Text1',
            'https://scontent-icn1-1.cdninstagram.com/t51.2885-19/s320x320/14719833_310540259320655_1605122788543168512_a.jpg',
            ['huntrax11', 'instagram']
        ),
        InstagramArticle(
            'Dummy Text2',
            'https://scontent-icn1-1.cdninstagram.com/t51.2885-19/s320x320/14719833_310540259320655_1605122788543168512_a.jpg',
            ['instagram', 'sup']
        ),
    ]


def get_user_likes_map(target_page_id, limit=None):
    '''인사타그램 유저-좋아요벡터맵을 가져옵니다 (클러스터링용)

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :return: {'follwer1':[True, False, ....], ...}
    :rtype: dict
    '''
    articles = get_articles(target_page_id, limit)
    users = sorted(reduce(set.union, map(attrgetter('liked_users'), articles)))
    return {user: [user in article.liked_users for article in articles]
            for user in users}
