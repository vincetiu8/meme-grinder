from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils.utils import make_dirs, move_memes, find, download_image
import time

class Reddit_Bot():
    def __init__(self, username, password, delay, desired_size, name_length):
        self.username = username
        self.password = password
        self.delay = delay
        self.desired_size = desired_size
        self.name_length = name_length

    def load_hyperlinks(self, sub = ''):
        make_dirs(['images', 'temp_images'])

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

        driver.quit()

    def loop_through_links(self, links):
        for link in links:
            if (link.get_attribute('href').find('https://www.reddit.com/r/') == 0):
                prevlink = link.get_attribute('href')
                try:
                    img = link.find_element_by_css_selector('img')
                except:
                    continue
                if img.get_attribute('alt').find('Post image') == -1:
                    continue
                url = img.get_attribute('src')
                if download_image(url, self.desired_size, self.name_length) == False:
                    return False
        return True

# For testing functionality
# bot = Reddit_Bot('invincbot', 'Frenchfri365', 5, 1024, 144)
# try:
#     bot.load_hyperlinks()
#
# except KeyboardInterrupt:
#     move_memes()
