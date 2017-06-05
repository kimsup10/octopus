from io import BytesIO
import requests
from PIL import Image


class InstagramArticle():
    '''Instagram Article'''

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

    def __init__(self, text, image_url, liked_users, likes_count,
                 commented_users, comments_count):
        self.text = text
        self.image_url = image_url
        self.liked_users = set(liked_users)
        self.likes_count = likes_count
        self.commented_users = set(commented_users)
        self.comments_count = comments_count

    @property
    def image(self):
        resp = requests.get(self.image_url)
        return Image.open(BytesIO(resp.content))

    @property
    def engaged_users(self):
        return self.liked_users | self.commented_users

    def __repr__(self):
        return repr(self.__dict__)
