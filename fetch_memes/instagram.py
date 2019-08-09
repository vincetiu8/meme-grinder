from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
import time
import requests
import math
from PIL import Image
import imagehash
import atexit
from pathlib import PureWindowsPath, Path

class Instagram_Bot():
    def __init__(self, username, password, delay, desired_size, hash_length):
        self.username = username
        self.password = password
        self.delay = delay
        assert(desired_size > 0)
        self.desired_size = desired_size
        assert(math.sqrt(hash_length).is_integer())
        self.hash_size = int(math.sqrt(hash_length) * 2)

    def load_hyperlinks(self):
        self.img_path = Path('./images')
        if not self.img_path.exists():
            self.img_path.mkdir()

        self.temp_img_path = Path('./temp_images')
        if not self.temp_img_path.exists():
            self.temp_img_path.mkdir()

        atexit.register(self.move_memes)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications' : 2})
        # For testing functionality
        # chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome('D:/Vince/Documents/chromedriver.exe', chrome_options = chrome_options)
        driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(self.delay)
        emailInput = driver.find_elements_by_css_selector('form input')[0]
        passwordInput = driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(self.delay)
        if len(driver.find_elements_by_css_selector('div[role="presentation"] button')) > 0:
            notification = driver.find_elements_by_css_selector('div[role="presentation"] button')[1]
            notification.click()
            time.sleep(self.delay)

        while True:
            images = driver.find_elements_by_css_selector('article img')
            if self.loop_through_images(images) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(self.delay)

        self.move_memes()
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

        old_size = i.size
        if old_size[0] / 2 > old_size[1] or old_size[0] < old_size[1] / 2:
            return True

        ratio = float(self.desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        i = i.resize(new_size, Image.ANTIALIAS)

        new_i = Image.new("RGB", (self.desired_size, self.desired_size))
        new_i.paste(i, ((self.desired_size - new_size[0]) // 2, (self.desired_size - new_size[1]) // 2))

        hash = str(imagehash.phash(new_i, self.hash_size))
        if self.find(self.img_path, hash, '.png'):
            return False
        if self.find(self.temp_img_path, hash, '.png'):
            return True

        new_i.save('./temp_images/' + hash + '.png')
        del response
        return True

    def move_memes(self):
        if self.temp_img_path != None and self.temp_img_path.exists() == True:
            for img in self.temp_img_path.glob('**/*.png'):
                shutil.copyfile(img, PureWindowsPath(self.img_path, img.name))
                img.unlink()
            self.temp_img_path.rmdir()

    def find(self, path, id, type):
        if len(list(path.glob('**/' + id + type))) > 0:
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
# bot = Instagram_Bot('mustardmayonaiseketchup', 'Frenchfri365', 5, 1024, 144)
# bot.load_hyperlinks()
