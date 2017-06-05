class InstagramUser():
    '''Instagram User'''

    '''Instagram ID'''
    id_ = None

    '''Instagram 계정명'''
    username = None

    '''프로필 사진'''
    profile_pic_url = None

    def __init__(self, id_=None, username=None, profile_pic_url=None,
                 **kwargs):
        self.id_ = kwargs.get('id', id_)
        self.username = kwargs.get('username', username)
        self.profile_pic_url = kwargs.get('profile_pic_url', profile_pic_url)

    def __eq__(self, other):
        return self.id_ == other.id_

    def __lt__(self, other):
        return self.id_ < other.id_

    def __repr__(self):
        return self.username

    def __hash__(self):
        return hash(self.id_)
