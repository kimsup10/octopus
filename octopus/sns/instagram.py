from functools import lru_cache
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .user import InstagramUser
from .article import InstagramArticle


class InstagramAPI():
    def __init__(self, username, password):
        self.driver = Chrome()
        self.authenticate(username, password)

    def get_shared_data(self, key):
        return self.driver.execute_script(
            'return window._sharedData.entry_data'
        )[key][0]['graphql']

    def authenticate(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        user_field = self.driver.find_element_by_name('username')
        user_field.clear()
        user_field.send_keys(username)
        pass_field = self.driver.find_element_by_name('password')
        pass_field.clear()
        pass_field.send_keys(password)
        self.driver.find_element_by_tag_name('form').submit()
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'nav a[class*=NavProfile]'
            ))
        )
        self.user = InstagramUser(**self.get_shared_data('FeedPage')['user'])
        self.username = self.user.username

    @lru_cache()
    def get_articles(self, username=None):
        if username is None:
            username = self.user.username
        self.driver.get('https://www.instagram.com/%s' % username)
        try:
            self.driver.find_element_by_link_text('Load more').click()
        except NoSuchElementException:
            pass
        imgs = self.driver.find_elements_by_css_selector('main a[href^="/p/"]')
        imgs = list(map(lambda img: img.get_attribute('href'), imgs))
        r = []
        for img in imgs:
            self.driver.get(img)
            m = self.get_shared_data('PostPage')['shortcode_media']
            r.append(InstagramArticle(
                InstagramUser(**m['owner']),
                ''.join(map(lambda e: e['node']['text'],
                            m['edge_media_to_caption']['edges'])),
                m['display_url'],
                map(lambda e: InstagramUser(**e['node']),
                    m['edge_media_preview_like']['edges']),
                m['edge_media_preview_like']['count'],
                map(lambda e: InstagramUser(**e['node']['owner']),
                    m['edge_media_to_comment']['edges']),
                m['edge_media_to_comment']['count']
            ))
        return r
