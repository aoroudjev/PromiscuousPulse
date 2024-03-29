from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


def start_driver():
    # returns headless driver
    options = Options()
    options.headless = False
    options.EnableVerboseLogging = True
    options.add_argument("--mute-audio")
    return uc.Chrome(options=options)
