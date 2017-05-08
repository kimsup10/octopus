from instagram import InstagramAPI


def get_articles(target_page_id):
    '''인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :return: [(article, [liked_users, ...])]
    :rtype: list
    '''
    raise NotImplementedError()


def get_user_likes_map(target_page_id):
    '''인스타그램 게시물을 가져옵니다

    :param target_page_id: 타겟 페이지 ID ex) huntrax11
    :return: {'follwer1':[True, False, ....], ...}
    :rtype: dict
    '''
    raise NotImplementedError()
