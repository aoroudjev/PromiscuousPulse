import time

import selenium.webdriver.ie.webdriver
from undetected_chromedriver import By


def login(driver: selenium.webdriver.ie.webdriver.WebDriver, credentials: dict, first_login=False):
    driver.get('https://app.member.virginpulse.com/#/home')
    time.sleep(5)
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input') if
                      elem.accessible_name.lower() in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name.lower())])
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(10)
    if driver.title != "Virgin Pulse - Home":
        raise ValueError


def do_dailies(driver):
    driver.get("https://app.member.virginpulse.com/#/healthyhabits")
    time.sleep(5)

    bttn_elements = [elem for elem in driver.find_elements(By.TAG_NAME, "button") if
                     elem.accessible_name.lower() == "yes"]
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, "input")]
    for button in bttn_elements:
        button.click()
    print('stop')
