from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import os
import time
import requests
import math
from PIL import Image
import imagehash
import atexit

class Reddit_Bot():
    def __init__(self, username, password, delay, desired_size, hash_length):
        self.username = username
        self.password = password
        self.delay = delay
        assert(desired_size > 0)
        self.desired_size = desired_size
        assert(math.sqrt(hash_length).is_integer())
        self.hash_size = int(math.sqrt(hash_length) * 2)

    def load_hyperlinks(self, sub = ''):
        if not self.find('images', './'):
            os.mkdir('./images')

        if not self.find('temp_images', './'):
            os.mkdir('./temp_images')

        atexit.register(self.move_memes)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})

        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe', chrome_options=chrome_options)
        driver.get('https://www.reddit.com/login/')

        time.sleep(self.delay)
        emailInput = driver.find_elements_by_css_selector('form fieldset input')[0]
        passwordInput = driver.find_elements_by_css_selector('form fieldset input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(self.delay)
        if sub != '':
            driver.get('https://www.reddit.com/' + sub)

        time.sleep(self.delay)
        while True:
            links = driver.find_elements_by_css_selector('a')
            if self.loop_through_links(links) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(self.delay)

        self.move_memes()
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

        old_size = i.size
        if old_size[0] / 2 > old_size[1] or old_size[0] < old_size[1] / 2:
            return True

        ratio = float(self.desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        i = i.resize(new_size, Image.ANTIALIAS)

        new_i = Image.new("RGB", (self.desired_size, self.desired_size))
        new_i.paste(i, ((self.desired_size - new_size[0]) // 2, (self.desired_size - new_size[1]) // 2))

        hash = str(imagehash.phash(new_i, self.hash_size))
        if self.find(hash, 'images'):
            return False
        if self.find(hash, 'temp_images'):
            return True

        new_i.save('temp_images/' + hash + '.png')
        del response
        return True

    def move_memes(self):
        if self.find('temp_images', './'):
            for img in os.listdir('temp_images'):
                shutil.copyfile('temp_images/' + img, 'images/' + img)
            shutil.rmtree('temp_images')

    def find(self, id, path):
        for filename in os.listdir(path):
            if filename.startswith(id):
                return True

        return False

# For testing functionality
# bot = Reddit_Bot('invincbot', 'Frenchfri365', 5, 1024, 144)
# bot.load_hyperlinks()
