from io import BytesIO
from operator import itemgetter
import requests
from PIL import Image


class InstagramArticle():
    '''Instagram Article'''

    '''Instagram 글'''
    text = None

    '''Instagram 사진 URL'''
    image_url = None

    '''글 좋아한 유저 목록'''
    liked_users = None

    def __init__(self, text, image_url, liked_users=[]):
        self.text = text
        self.image_url = image_url
        self.liked_users = set(liked_users)

    @property
    def image(self):
        resp = requests.get(self.image_url)
        return Image.open(BytesIO(resp.content))

    @staticmethod
    def from_media(api, media):
        return InstagramArticle(
            (media['caption'] or {}).get('text', ''),
            media['images']['standard_resolution']['url'],
            map(itemgetter('id'), api.get_likes(media['id'])['data'])
        )

    def __repr__(self):
        return repr(self.__dict__)
