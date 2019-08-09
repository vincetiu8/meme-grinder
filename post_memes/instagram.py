from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import PureWindowsPath, Path
import shutil
import time
import requests
import autoit

class Instagram_Bot():
    def __init__(self, email, password, delay, post_delay):
        self.email = email
        self.password = password
        self.delay = delay
        self.post_delay = post_delay

    def post_memes(self):
        self.img_path = Path('./memes_to_be_posted')
        if not self.img_path.exists():
            return
        print(self.img_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 2"})
        chrome_options.add_argument("--start-maximized")
        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe', chrome_options = chrome_options)
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(self.delay)

        email_input = driver.find_elements_by_css_selector('form input')[0]
        password_input = driver.find_elements_by_css_selector('form input')[1]
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(self.delay)

        # Code if email input needed
        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        # driver.get('https://mail.google.com')
        #
        # time.sleep(self.delay)
        # email_input = driver.find_elements_by_css_selector('form input')[0]
        # email_input.send_keys(self.email)
        # email_input.send_keys(Keys.ENTER)
        #
        # time.sleep(self.delay)
        # for element in driver.find_elements_by_css_selector('form input'):
        #     print(element.get_attribute('type'))
        # password_input = driver.find_elements_by_css_selector('form input')[2]
        # password_input.send_keys(self.password)
        # password_input.send_keys(Keys.ENTER)
        #
        # time.sleep(self.delay)
        # driver.find_element_by_css_selector('a').click()

        notification = driver.find_elements_by_css_selector('div[role="presentation"] button')[2]
        notification.click()
        time.sleep(self.delay)

        for file in list(self.img_path.glob('**/*')):
            add_post = driver.find_element_by_css_selector('nav div[role="menuitem"]')
            add_post.click()
            time.sleep(self.delay)

            autoit.win_wait("[CLASS:#32770;TITLE:Open]", 20)
            _path = str(file.absolute())
            path = _path[:len(_path) - _path.find('D:')]
            print(path)
            time.sleep(0.5)
            autoit.control_send("[CLASS:#32770;TITLE:Open]", "Edit1", path)
            time.sleep(0.5)
            autoit.control_click("[CLASS:#32770;TITLE:Open]", "Button1")
            time.sleep(self.delay)

            next_button = driver.find_elements_by_css_selector('header button')[1]
            next_button.click()
            time.sleep(self.delay)

            text_area = driver.find_elements_by_css_selector('textarea')[0]
            text_area.send_keys('#dankmemes #dankmeme #memes #meme #memes2good #memesdaily #memesquad #memestagram #memeslayer #memesrlife #memes4days #memestgram #memess #memestar #memesdank #memesfordays #spicymemes #funny')
            share_button = driver.find_elements_by_css_selector('header button')[1]
            share_button.click()
            file.unlink()
            time.sleep(self.post_delay)

        driver.quit()

    def find(self, id, path):
        for filename in os.listdir(path):
            if filename.startswith(id):
                return True

        return False

bot = Instagram_Bot('mustardmayonaiseketchup@gmail.com', 'Frenchfri365', 6, 1800)
bot.post_memes()
