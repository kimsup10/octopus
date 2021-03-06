import os
import hashlib
import requests
from PIL import Image
from ..preprocessing import process


class InstagramArticle():
    '''Instagram Article'''

    '''Article 작성자'''
    user = None

    '''Instagram 글'''
    text = None

    '''Instagram 사진 URL'''
    image_url = None

    '''좋아요 수'''
    likes_count = None

    '''글 좋아한 유저 목록'''
    liked_users = None

    '''댓글 수'''
    comments_count = None

    '''글에 댓글 단 유저 목록'''
    commented_users = None

    def __init__(self, user, text, image_url, liked_users, likes_count,
                 commented_users, comments_count):
        self.user = user
        self.text = text
        self.image_url = image_url
        self.liked_users = set(liked_users)
        self.likes_count = likes_count
        self.commented_users = set(commented_users)
        self.comments_count = comments_count

    @property
    def image(self):
        filename = 'data/img/%s-%s' % (
            self.user.username,
            hashlib.sha1(self.image_url.encode()).hexdigest()
        )
        if not os.path.isfile(filename):
            resp = requests.get(self.image_url)
            with open(filename, 'wb') as f:
                f.write(resp.content)
        return Image.open(filename)

    @property
    def engaged_users(self):
        return self.liked_users | self.commented_users

    @property
    def tokens(self):
        if hasattr(self, '_tokens'):
            return self._tokens
        self._tokens = set(process(self.text))
        try:
            self._tokens |= set(process(self.image))
        except Exception:
            pass
        return self._tokens

    def __repr__(self):
        return repr(self.__dict__)
