import os
import time
import pickle

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from init_driver import get_chrome_driver
from media_db_interface import MediaDBInterface

load_dotenv()

INSTAGRAM_LOGIN = os.getenv('INSTAGRAM_LOGIN')
INSTAGRAM_PASS = os.getenv('INSTAGRAM_PASS')


class InstagramParser:
    instagram_url = 'https://instagram.com'
    driver = get_chrome_driver(use_proxy=True)
    media_db_interface = MediaDBInterface()

    texts = []
    @classmethod
    def instagram_first_login(cls):
        cls.driver.get(cls.instagram_url)
        time.sleep(1)

        login_input = cls.driver.find_element(By.NAME, 'username')
        password_input = cls.driver.find_element(By.NAME, 'password')

        login_input.send_keys(INSTAGRAM_LOGIN)
        password_input.send_keys(INSTAGRAM_PASS)
        time.sleep(0.5)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)

        cls.create_cookies_folder()
        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'wb') as pc:
            pickle.dump(cls.driver.get_cookies(), pc)
        print(f'==========\nКуки для {INSTAGRAM_LOGIN} сохранены\n==========')

    @classmethod
    def create_cookies_folder(cls):
        if not 'cookies' in os.listdir():
            os.mkdir('cookies')

    @classmethod
    def instagram_login(cls):
        cls.driver.get(cls.instagram_url)
        time.sleep(1)

        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'rb') as pc:
            cookies = pickle.load(pc)

        for cookie in cookies:
            print(cookie)
            cls.driver.add_cookie(cookie)

    @classmethod
    def get_post_urls(cls, bar_name):
        url = cls.media_db_interface.get_media_url_by_bar_name(bar_name, 'inst')

        cls.driver.get(url)
        time.sleep(1)

        cls.driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)

        elements = cls.driver.find_elements(By.TAG_NAME, 'a')
        post_urls = [x.get_attribute('href') for x in elements if '/p/' in x.get_attribute('href')]
        return post_urls

    @classmethod
    def save_bar_post_text(cls, bar_name):
        post_urls = cls.get_post_urls(bar_name)
        time.sleep(1)
        bar_post_texts = []
        for post_url in post_urls:
            cls.driver.get(post_url)
            time.sleep(4)
            elements = cls.driver.find_elements(By.TAG_NAME, 'span')
            for elem in elements:
                if elem.find_elements(By.TAG_NAME, 'br'):
                    bar_post_texts.append(elem.text)
            time.sleep(1)
        return bar_post_texts


    @classmethod
    def save_all_bars_text(cls):
        bars_name = cls.media_db_interface.get_all_bar_names()
        for bar_name in bars_name:
            bar_post_texts = cls.save_bar_post_text(bar_name)
            with open('all_bars_posts.txt', 'a', encoding='utf-8') as f:
                f.write(f'{bar_name}\n')
                for text in bar_post_texts:
                    f.write(f'{text}\n')

if __name__ == '__main__':
    #name = 'Sgt. PEPPER’S bar'
    InstagramParser.instagram_first_login()
    InstagramParser.save_all_bars_text()
