from urllib.parse import urlencode
import requests
from .. import config


API_BASE = 'https://api.instagram.com'


class InstagramAPI():
    def __init__(self):
        # TODO: proper implementation
        self.token = config['instagram']['access_token']

    def authenticate(self):
        if self.token:
            return self.token
        client_id = config['instagram']['client_id']
        url = API_BASE + '/oauth/authorize?' \
            + urlencode({
                'client_id': client_id,
                'redirect_uri': 'https://devel.huntrax.com/ouath/',
                'response_type': 'token',
                'scope': 'public_content'
            })
        # TODO: proper implementation
        print(url)
        self.token = input('Token: ').strip()
        return self.token

    def find_user(self, username):
        resp = requests.get(API_BASE+'/v1/users/search', params={
            'access_token': self.token,
            'q': username,
        })
        users = list(filter(lambda u: u['username'] == username,
                            resp.json()['data']))
        if users:
            return users[0]

    def get_recent_media(self, username=None):
        if username:
            user_id = self.find_user(username)['id']
            resp = requests.get(
                API_BASE+'/v1/users/%s/media/recent/' % (user_id, ),
                params={
                    'access_token': self.token,
                })
        else:
            resp = requests.get(
                API_BASE+'/v1/users/self/media/recent/',
                params={
                    'access_token': self.token,
                })
        return resp.json()

    def get_likes(self, media_id):
        resp = requests.get(
            API_BASE+'/v1/media/%s/likes' % (media_id, ),
            params={
                'access_token': self.token,
            })
        return resp.json()
