import os
import time

from os import path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Screenshotter():
    driver = None

    def __del__(self) -> None:
        driver.quit()

    def init_driver(self, selniumserver) -> None:
        # initialize the driver that connects to the selenium container
        options = Options()
        options.headless = True
        options.add_argument("--log-level=3")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4501.0 Safari/537.36 Edg/92.0.891.1')

        global driver

        driver = webdriver.Remote(
            options=options,
            command_executor=selniumserver,
            desired_capabilities=DesiredCapabilities.CHROME)

        window_size = driver.execute_script("""
                            return [window.outerWidth - window.innerWidth + arguments[0],
                                window.outerHeight - window.innerHeight + arguments[1]];
                            """, 1650, 4250)
        driver.set_window_size(*window_size)


    def screenshot(self, tweet) -> str:
        username = tweet.author.screen_name
        id = str(tweet.id)

        driver.get(f"https://twitter.com/{username}/status/{id}")

        time.sleep(3) #really? Yes, really! Need this time to load data async.
        driver.execute_script("window.scrollTo(0, 0);")

        datadir = f"data/{username}/"
        if not path.isdir(datadir):
            os.makedirs(datadir)

        driver.save_screenshot(f"{datadir}page.png")
        element = driver.find_element_by_css_selector(
            'article[data-testid="tweet"]:not([tabindex])')  # :not([tabindex])

        location = element.location
        size = element.size
        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']

        im = Image.open(f"{datadir}page.png")
        im = im.crop((int(x), int(y), int(width), int(height)))

        p = f"{datadir}screenshots/{tweet.created_at.strftime('%m')}/{tweet.created_at.strftime('%d')}"

        if not path.isdir(p):
            os.makedirs(p)

        im.save(f"{p}/{id}.png")

        return f"{p}/{id}.png"
