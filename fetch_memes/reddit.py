from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import os
import time
import requests
from PIL import Image
import imagehash

class Reddit_Bot():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def init_directory(self):
        if not os.path.isdir('./images'):
            os.mkdir('./images')

    def load_hyperlinks(self, sub = ''):
        if not os.path.isdir('./temp_images'):
            os.mkdir('./temp_images')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})

        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe', chrome_options=chrome_options)
        driver.get('https://www.reddit.com/login/')

        time.sleep(1.5)
        emailInput = driver.find_elements_by_css_selector('form fieldset input')[0]
        passwordInput = driver.find_elements_by_css_selector('form fieldset input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(5)
        driver.get('https://www.reddit.com/' + sub + '/')

        time.sleep(5)
        while True:
            links = driver.find_elements_by_css_selector('a')
            if self.loop_through_links(links) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(5)

        for img in os.listdir('temp_images'):
            shutil.copyfile('temp_images/' + img, 'images/' + img)
        driver.quit()

    def loop_through_links(self, links):
        for link in links:
            if (link.get_attribute('href').find('https://www.reddit.com/r/') == 0
            ):
                prevlink = link.get_attribute('href')
                try:
                    img = link.find_element_by_css_selector('img')
                except:
                    continue
                if img.get_attribute('alt').find('Post image') == -1:
                    continue
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

# For testing functionality
# bot = Reddit_Bot('invincbot', 'frenchfri')
# bot.init_directory()
# bot.load_hyperlinks('r/dankmemes')
