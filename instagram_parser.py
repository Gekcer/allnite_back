import os
import time
import pickle

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sqlalchemy import select
from init_driver import get_chrome_driver

load_dotenv()

DB_FOLDER = os.getenv('DB_FOLDER')
DB_NAME = os.getenv('DB_NAME')
DB_URL = f'sqlite:///{os.path.join(DB_FOLDER, DB_NAME)}'

INSTAGRAM_LOGIN = os.getenv('INSTAGRAM_LOGIN')
INSTAGRAM_PASS = os.getenv('INSTAGRAM_PASS')


class InstagramParser:
    @classmethod
    def instagram_first_login(cls, driver, url):
        driver.get(url)
        time.sleep(1)

        login_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')

        login_input.send_keys(INSTAGRAM_LOGIN)
        password_input.send_keys(INSTAGRAM_PASS)
        time.sleep(0.5)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)

        cls.create_cookies_folder()
        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'wb') as pc:
            pickle.dump(driver.get_cookies(), pc)
        print(f'==========\nКуки для {INSTAGRAM_LOGIN} сохранены\n==========')

    @classmethod
    def create_cookies_folder(cls):
        if not 'cookies' in os.listdir():
            os.mkdir('cookies')

    @classmethod
    def instagram_login(cls, driver, url):
        driver.get(url)
        time.sleep(1)

        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'rb') as pc:
            cookies = pickle.load(pc)

        for cookie in cookies:
            print(cookie)
            driver.add_cookie(cookie)



if __name__ == '__main__':
    driver = get_chrome_driver(True)
    url = 'https://instagram.com'
    InstagramParser.instagram_first_login(driver, url)