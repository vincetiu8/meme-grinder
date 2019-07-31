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

    def load_hyperlinks(self, account):
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
        driver.get('https://www.instagram.com/' + account + '/?hl=en')

        time.sleep(1.5)
        driver.find_element_by_css_selector('article a').click()

        while True:
            time.sleep(1)
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break

            time.sleep(1)
            next = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
            next.click()

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
                print(url)
                if self.download_image(url) == False:
                    return False
        return True

    def download_image(self, url):
        id = url[url.find('vp/') + 3:url.find('/t51') - 9]
        print(id)
        if self.find(id):
            return False
        response = requests.get(url, stream=True)
        with open('./images/' + id + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return True


    def find(self, id):
        for filename in os.listdir('images'):
            if filename.startswith(id):
                return True

        return False

bot = Bot()
bot.init_directory()
bot.load_hyperlinks('mustardmayonaiseketchup')
