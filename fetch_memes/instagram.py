from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import os
import time
import requests
from PIL import Image
import imagehash

class Instagram_Bot():
    def __init__(self, username, password, delay):
        self.username = username
        self.password = password
        self.delay = delay

    def load_hyperlinks(self):
        if not os.path.isdir('./images'):
            os.mkdir('./images')

        if not os.path.isdir('./temp_images'):
            os.mkdir('./temp_images')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})
        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe')
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(self.delay)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(self.delay)
        notification = driver.find_elements_by_css_selector('div[role="presentation"] button')[1]
        notification.click()

        time.sleep(self.delay)
        while True:
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(self.delay)

        if self.find('temp_images', './'):
            for img in os.listdir('temp_images'):
                shutil.copyfile('temp_images/' + img, 'images/' + img)
            shutil.rmtree('temp_images')

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

class Instagram_Page_Bot(Instagram_Bot):
    def load_hyperlinks(self, account):
        # For testing functionality
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe')
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(self.delay)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(self.delay)
        driver.get('https://www.instagram.com/' + account + '/?hl=en')

        time.sleep(self.delay)
        driver.find_element_by_css_selector('article a').click()

        while True:
            time.sleep(self.delay)
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break

            time.sleep(self.delay)
            next = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
            next.click()

        driver.quit()

# For testing functionality
# bot = Instagram_Bot('mustardmayonaiseketchup', 'frenchfri')
# bot.init_directory()
# bot.load_hyperlinks()
# bot = Instagram_Page_Bot('mustardmayonaiseketchup', 'frenchfri')
# bot.load_hyperlinks('mustardmayonaiseketchup')
