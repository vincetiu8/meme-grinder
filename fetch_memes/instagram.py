from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils.utils import make_dirs, move_memes, find, download_image
import time

class Instagram_Bot():
    def __init__(self, username, password, delay, desired_size, name_length):
        self.username = username
        self.password = password
        self.delay = delay
        self.desired_size = desired_size
        self.name_length = name_length

    def load_hyperlinks(self):
        make_dirs(['images', 'temp_images'])

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
            if self.loop_through_links(images) == False:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(self.delay)

        self.move_memes()
        driver.quit()


    def loop_through_links(self, images):
        for img in images:
            if (
                (
                    img.get_attribute('alt').find('Image') != -1
                    or img.get_attribute('alt').find('photo') != -1
                )
                and img.get_attribute('srcset').find('1080w') != -1
            ):
                url = img.get_attribute('src')
                if download_image(url, self.desired_size, self.name_length) == False:
                    return False
        return True

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
            if self.loop_through_links(images) == False:
                break

            time.sleep(self.delay)
            next = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
            next.click()

        driver.quit()

# For testing functionality
# bot = Instagram_Bot('invincbot', 'Frenchfri365', 5, 1024, 144)
# try:
#     bot.load_hyperlinks()
#
# except KeyboardInterrupt:
#     move_memes()
