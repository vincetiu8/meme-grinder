from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import os
import time
import requests

class Bot():
    def __init__(self):
        self.username = 'mustardmayonaiseketchup'
        self.password = 'frenchfri'
        self.images = []

    def init_directory(self):
        if not os.path.isdir('./images'):
            os.mkdir('./images')

    def load_hyperlinks(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe')
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(1.5)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(1.5)
        notification = driver.find_elements_by_css_selector('div[role="presentation"] button')[1]
        notification.click()

        time.sleep(1.5)
        for img in driver.find_elements_by_css_selector('article img'):
            if img.get_attribute('alt').find('photo') != -1 or img.get_attribute('alt').find('Image') != -1:
                srcset = img.get_attribute('srcset')
                self.images.append(srcset[:srcset.find('640w') - 1])
                print(srcset[:srcset.find('640w')])

    def download_images(self):
        for url in self.images:
            id = url[url.find('x640') + 5:url.find('.jpg') - 2]
            print(id)
            if self.find(id):
                continue
            response = requests.get(url, stream=True)
            with open('./images/' + id + '.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response


    def find(self, id):
        for filename in os.listdir('images'):
            if filename.startswith(id):
                return True

        return False

bot = Bot()
bot.init_directory()
bot.load_hyperlinks()
bot.download_images()
