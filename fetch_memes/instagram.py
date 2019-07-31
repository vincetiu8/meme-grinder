from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import os
import time
import requests

class Instagram_Bot():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def init_directory(self):
        if not os.path.isdir('./images'):
            os.mkdir('./images')

    def load_hyperlinks(self):
        if not os.path.isdir('./temp_images'):
            os.mkdir('./temp_images')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})
        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe')
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(1.5)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(3)
        notification = driver.find_elements_by_css_selector('div[role="presentation"] button')[1]
        notification.click()

        time.sleep(1)
        while True:
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(5)

        for img in os.listdir('temp_images'):
            shutil.copyfile('temp_images/' + img, 'images/' + img)

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
        id = url[url.find('vp/') + 3:url.find('/t51') - 9]
        if self.find(id, 'images'):
            return False
        if self.find(id, 'temp_images'):
            return True

        response = requests.get(url, stream=True)
        with open('./temp_images/' + id + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return True

    def find(self, id, path):
        for filename in os.listdir(path):
            if filename.startswith(id):
                return True

        return False

class Instagram_Page_Bot(Instagram_Bot):
    def load_hyperlinks(self, account):
        # For testing functionality
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe')
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(1)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(2)
        driver.get('https://www.instagram.com/' + account + '/?hl=en')

        time.sleep(2)
        driver.find_element_by_css_selector('article a').click()

        while True:
            time.sleep(1)
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break

            time.sleep(1)
            next = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
            next.click()

        driver.quit()

# For testing functionality
bot = Instagram_Bot('mustardmayonaiseketchup', 'frenchfri')
bot.init_directory()
bot.load_hyperlinks()
# bot = Instagram_Page_Bot('mustardmayonaiseketchup', 'frenchfri')
# bot.load_hyperlinks('mustardmayonaiseketchup')
