import time

import selenium.webdriver.ie.webdriver
from selenium.webdriver.common.keys import Keys

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


def track_habits(driver):
    responses = {
        "minutes": "60",
        "enter duration in minutes": "60",
        "enter hours of sleep": "8",
        "enter number of steps": "30000",
    }
    driver.get("https://app.member.virginpulse.com/#/healthyhabits")
    time.sleep(5)

    button_elements = [elem for elem in driver.find_elements(By.TAG_NAME, "button") if
                       elem.accessible_name.lower() == "yes"]
    for button in button_elements:
        button.click()

    # Write out activity to display hidden items
    activity = [elem for elem in driver.find_elements(By.TAG_NAME, "input") if
                elem.accessible_name == "What activity did you do? Select an activity or start typing"]
    activity[0].send_keys("Badminton\ue007")

    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, "input")]
    for input_field in input_elements:
        if input_field.accessible_name.lower() in responses:
            input_field.send_keys(responses[str(input_field.accessible_name.lower())])

    time.sleep(2)

    button_elements = [elem for elem in driver.find_elements(By.TAG_NAME, "button") if
                       elem.accessible_name.lower() == "track it!"]

    # JS click instead after entry input
    for button in button_elements:
        driver.execute_script("arguments[0].click();", button)

