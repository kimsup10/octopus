from urllib.parse import urlencode
from requests import Session
from .. import config


API_BASE = 'https://api.instagram.com'


class InstagramAPI():
    def __init__(self):
        # TODO: proper implementation
        self.token = config['instagram']['access_token']
        self.session = Session()

    def authenticate(self):
        if self.token:
            return self.token
        client_id = config['instagram']['client_id']
        url = API_BASE + '/oauth/authorize?' \
            + urlencode({
                'client_id': client_id,
                'redirect_uri': 'https://devel.huntrax.com/oauth/',
                'response_type': 'token',
                'scope': 'public_content'
            })
        # TODO: proper implementation
        print(url)
        self.token = input('Token: ').strip()
        return self.token

    def check_envelope(self, resp):
        resp = resp.json()
        assert resp['meta']['code'] == 200, \
            'Invalid status code: %r' % resp['meta']
        yield from resp['data']
        if 'pagination' in resp and 'next_url' in resp['pagination']:
            resp = self.session.get(resp['pagination']['next_url'])
            yield from self.check_envelope(resp)

    def find_user(self, username):
        resp = self.session.get(API_BASE+'/v1/users/search', params={
            'access_token': self.token,
            'q': username,
        })
        resp = self.check_envelope(resp)
        return next(filter(lambda u: u['username'] == username, resp))

    def get_recent_media(self, username=None):
        if username:
            user_id = self.find_user(username)['id']
            resp = self.session.get(
                API_BASE+'/v1/users/%s/media/recent/' % (user_id, ),
                params={
                    'access_token': self.token,
                })
        else:
            resp = self.session.get(
                API_BASE+'/v1/users/self/media/recent/',
                params={
                    'access_token': self.token,
                })
        resp = self.check_envelope(resp)
        return resp

    def get_likes(self, media_id):
        resp = self.session.get(
            API_BASE+'/v1/media/%s/likes' % (media_id, ),
            params={
                'access_token': self.token,
            })
        resp = self.check_envelope(resp)
        return resp
