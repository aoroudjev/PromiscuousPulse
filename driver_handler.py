from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

def start_driver() -> webdriver:
    # returns headless driver
    options = Options()
    options.headless = True
    options.EnableVerboseLogging = True
    return uc.Chrome(options=options)
