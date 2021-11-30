import os
import time
import datetime

from os import path
from PIL import Image
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Screenshotter():

    driver = None

    def __init__(self):
        self.init_driver()

    def __del__(self):
        driver.quit()

    def init_driver(self):
        # initialize the driver that connects to the selenium container
        #print('Init driver')

        options = Options()
        options.headless = True
        options.add_argument("--log-level=3")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4501.0 Safari/537.36 Edg/92.0.891.1')

        global driver
        driver = webdriver.Remote(
            options=options,
            command_executor='http://{}:4444/wd/hub'.format('192.168.100.10'),
            desired_capabilities=DesiredCapabilities.CHROME)

    def screenshot(self, id):
        window_size = driver.execute_script("""
                    return [window.outerWidth - window.innerWidth + arguments[0],
                        window.outerHeight - window.innerHeight + arguments[1]];
                    """, 650, 2250)
        driver.set_window_size(*window_size)

        driver.get(f"https://twitter.com/thierrybaudet/status/{id}")
        time.sleep(5)

        driver.save_screenshot("pdata/age.png")
        element = driver.find_element_by_css_selector('article[data-testid="tweet"]')

        location = element.location
        size = element.size
        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']
        im = Image.open('data/page.png')
        im = im.crop((int(x), int(y), int(width), int(height)))

        d = datetime.datetime.now()
        p = f"data/screenshots/{d.strftime('%m')}/{d.strftime('%d')}"

        if not path.isdir(p):
            os.makedirs(p)

        im.save(f"{p}/{id}.png")