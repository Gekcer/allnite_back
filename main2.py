import os
import time
import pickle

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

INSTAGRAM_LOGIN = os.getenv('INSTAGRAM_LOGIN')
INSTAGRAM_PASS = os.getenv('INSTAGRAM_PASS')


def instagram_first_login(driver, url):
    driver.get(url)
    time.sleep(1)

    # логин
    login_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    login_input.send_keys(INSTAGRAM_LOGIN)
    password_input.send_keys(INSTAGRAM_PASS)
    time.sleep(0.5)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)
    # сохранение куки
    create_cookies_folder()
    with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'wb') as pc:
        pickle.dump(driver.get_cookies(), pc)
    print(f'==========\nКуки для {INSTAGRAM_LOGIN} сохранены\n==========')


def create_cookies_folder():
    if not 'cookies' in os.listdir():
        os.mkdir('cookies')


def instagram_login(driver, url):
    driver.get(url)
    time.sleep(1)

    with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'rb') as pc:
        cookies = pickle.load(pc)

    for cookie in cookies:
        print(cookie)
        driver.add_cookie(cookie)
