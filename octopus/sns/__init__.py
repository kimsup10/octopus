from functools import reduce
from operator import attrgetter
from .article import InstagramArticle
from instagram import InstagramAPI

api = InstagramAPI(client_secret="6c1e32e9870b48ff85df24a63692097d".encode('utf-8'),
                   access_token="1372890096.0d8454c.e8a6723c2f864fd683582700e0c14aaf".encode("utf-8"))


def get_articles(target_page_id, limit=None):
    '''인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :param limit: 갯수 제한
    :return: list of `octopus.instagram.InstagramArticle`
    :rtype: list
    '''
    if limit is None:
        limit = 100
    articles_info, next_ = api.user_recent_media(target_page_id)
    print(111)
    while next_:
        more_articles_info, next_ = api.user_recent_media(with_next_url=next_)
        articles_info.extend(more_articles_info)

    articles = list(map(lambda media: InstagramArticle(media.caption.text,
                                                       media.images["standard_resolution"],
                                                       list(map(lambda user_info: user_info.username,
                                                                api.media_likes(media.id)))), articles_info))

    return articles


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
    # TODO: get_articles 구현후 변경하기 cc. @kimsup10
    articles = get_articles(target_page_id, limit)
    users = sorted(reduce(set.union, map(attrgetter('liked_users'), articles)))
    return {user: [user in article.liked_users for article in articles]
            for user in users}
