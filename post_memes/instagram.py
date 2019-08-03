from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import ntpath
import os
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
        if not ntpath.isdir('./memes_to_be_posted'):
            return

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

        while len(os.listdir('memes_to_be_posted')) > 0:
            add_post = driver.find_element_by_css_selector('nav div[role="menuitem"]')
            add_post.click()
            time.sleep(self.delay)

            autoit.win_wait("[CLASS:#32770;TITLE:Open]", 20)
            path = ntpath.realpath('./memes_to_be_posted/' + os.listdir('memes_to_be_posted')[0])
            time.sleep(0.5)
            autoit.control_send("[CLASS:#32770;TITLE:Open]", "Edit1", path)
            autoit.control_click("[CLASS:#32770;TITLE:Open]", "Button1")
            time.sleep(self.delay)

            for el in driver.find_elements_by_css_selector('header button'):
                print(el.get_attribute('innerHTML'))
            next_button = driver.find_elements_by_css_selector('header button')[1]
            next_button.click()
            time.sleep(self.delay)

            for el in driver.find_elements_by_css_selector('header button'):
                print(el.get_attribute('innerHTML'))
            share_button = driver.find_elements_by_css_selector('header button')[1]
            share_button.click()
            os.remove('./memes_to_be_posted/' + os.listdir('memes_to_be_posted')[0])
            time.sleep(self.post_delay)

        driver.quit()

    def loop_through_images(self, images):
        for img in images:
            if (
                (
                    img.get_attribute('alt').find('Image') != -1
                    or img.get_attribute('alt').find('photo') != -1
                )
                and img.get_attribute('srcset').find('1080w') != -1
            ):
                url = img.get_attribute('src')
                if self.download_image(url) == False:
                    return False
        return True

    def download_image(self, url):
        response = requests.get(url, stream = True)
        i = Image.open(response.raw)
        hash = str(imagehash.average_hash(i))
        if self.find(hash, 'images'):
            return False
        if self.find(hash, 'temp_images'):
            return True

        i.save('temp_images/' + hash + '.png')
        del response
        return True

    def find(self, id, path):
        for filename in os.listdir(path):
            if filename.startswith(id):
                return True

        return False

bot = Instagram_Bot('mustardmayonaiseketchup@gmail.com', 'Frenchfri365', 5, 600)
bot.post_memes()
