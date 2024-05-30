import os
import time
import pickle

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from init_driver import get_chrome_driver
from media_db_interface import MediaDBInterface

load_dotenv()

INSTAGRAM_LOGIN = os.getenv('INSTAGRAM_LOGIN')
INSTAGRAM_PASS = os.getenv('INSTAGRAM_PASS')


class InstagramParser:
    instagram_url = 'https://instagram.com'
    driver = get_chrome_driver(use_proxy=True, user_agent=True)
    media_db_interface = MediaDBInterface()

    texts = []
    @classmethod
    def instagram_first_login(cls):
        cls.driver.get(cls.instagram_url)
        time.sleep(3.32)

        elems = cls.driver.find_elements(By.TAG_NAME, 'button')
        for elem in elems:
            if 'Decline optional cookies' in elem.text:
                elem.click()
        time.sleep(3)

        login_input = cls.driver.find_element(By.NAME, 'username')
        password_input = cls.driver.find_element(By.NAME, 'password')

        login_input.send_keys(INSTAGRAM_LOGIN)
        time.sleep(3)
        password_input.send_keys(INSTAGRAM_PASS)
        time.sleep(3)
        password_input.send_keys(Keys.ENTER)

        cls.create_cookies_folder()
        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'wb') as pc:
            pickle.dump(cls.driver.get_cookies(), pc)
        print(f'==========\nКуки для {INSTAGRAM_LOGIN} сохранены\n==========')
        time.sleep(3)

    @classmethod
    def create_cookies_folder(cls):
        if not 'cookies' in os.listdir():
            os.mkdir('cookies')

    @classmethod
    def instagram_login(cls):
        cls.driver.get(cls.instagram_url)
        time.sleep(2.11)

        with open(os.path.join('cookies', f'{INSTAGRAM_LOGIN}_cookies'), 'rb') as pc:
            cookies = pickle.load(pc)

        for cookie in cookies:
            print(cookie)
            cls.driver.add_cookie(cookie)

    @classmethod
    def get_post_urls(cls, bar_name):
        url = cls.media_db_interface.get_media_url_by_bar_name(bar_name, 'inst')

        cls.driver.get(url)
        time.sleep(8)

        cls.driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(8)

        elements = cls.driver.find_elements(By.TAG_NAME, 'a')
        post_urls = [x.get_attribute('href') for x in elements if '/p/' in x.get_attribute('href') or '/reel/' in x.get_attribute('href')]
        time.sleep(8)
        return post_urls

    @classmethod
    def get_chunks(cls, chunk_size=4):
        bar_names = cls.media_db_interface.get_all_bar_names(media='inst')
        bar_names_chunks = [bar_names[x:x+chunk_size] for x in range(0, len(bar_names), chunk_size)]
        return bar_names_chunks

    @classmethod
    def save_bar_post_text(cls, bar_name):
        post_urls = cls.get_post_urls(bar_name)
        bar_post_texts = []
        bar_post_urls = []
        for post_url in post_urls:
            time.sleep(8)
            print(post_url)
            cls.driver.get(post_url)
            attempts = 0
            while attempts < 3:
                try:
                    element = WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
                    break
                except StaleElementReferenceException:
                    print(f'попытка {attempts+1}')
                    attempts += 1
                    continue
            else:
                print(f"Пропускаем {post_url} бара {bar_name}")
                continue
            #WebDriverWait(cls.driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))
            time.sleep(8)
            elements = cls.driver.find_elements(By.TAG_NAME, 'span')
            for elem in elements:
                try:
                    if elem.find_elements(By.TAG_NAME, 'br'):
                        bar_post_texts.append(elem.text)
                        bar_post_urls.append(post_url)
                except StaleElementReferenceException:
                    print(f"Элемент стал неактивным, {post_url}, {bar_name}")
                    continue
        return bar_post_texts, bar_post_urls


    @classmethod
    def save_all_bars_text(cls, chunk):
        for bar_name in chunk:
            data = []
            print(f'Запись бара {bar_name}')
            bar_post_texts, bar_post_urls = cls.save_bar_post_text(bar_name)
            for _ in range(len(bar_post_texts)):
                data.append({'bar_name': bar_name, 'bar_post_text': bar_post_texts[_], 'bar_post_url': bar_post_urls[_]})
            data_df = pd.DataFrame(data)
            bar_name_cleaned = bar_name.replace(',', '_').replace('?', '')
            data_df.to_csv(f'bar_texts_{bar_name_cleaned}.csv', encoding='utf_8')


    @classmethod
    def save_bar_post_screenshot(cls, bar_name):
        post_urls = cls.get_post_urls(bar_name)
        time.sleep(10)

        screenshots_folder = os.path.join(os.getcwd(), 'screenshots')
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)

        for post_url in post_urls:
            cls.driver.get(post_url)
            time.sleep(50)
            screen_name = os.path.join(screenshots_folder, f'{post_url.replace("/", "_").replace(":", "_")}.png')
            cls.driver.save_screenshot(screen_name)
            time.sleep(10)

if __name__ == '__main__':
    chunks = InstagramParser.get_chunks()
    chunks = chunks[0:3]
    for chunk in chunks:
        print(chunk)
    for i, chunk in enumerate(chunks):
        print(f'chunk num {i}')
        if i != 0:
            print('new_driver')
            InstagramParser.driver = get_chrome_driver(use_proxy=True, user_agent=True)
        InstagramParser.instagram_first_login()
        InstagramParser.save_all_bars_text(chunk)
        #InstagramParser.save_all_bars_text_alternative(chunk)
        InstagramParser.driver.quit()
        time.sleep(1)

    #InstagramParser.prepare_df_bar_texts(dfs)

