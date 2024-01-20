import time

import selenium.common
import undetected_chromedriver
from undetected_chromedriver import By


def login(driver: undetected_chromedriver.Chrome, credentials: dict, first_login=False):
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


def link_from_rewards(driver, link_text: str):
    driver.get("https://app.member.virginpulse.com/#/my-rewards/earn")
    time.sleep(7)
    driver.find_elements(By.LINK_TEXT, link_text)[0].click()
    time.sleep(5)


def do_assessment(driver: undetected_chromedriver.Chrome):
    driver.get("https://app.member.virginpulse.com/#/surveys-ui/surveys/47069/intro")
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       "button[id='survey-start-button']"))
    button = driver.find_element(By.TAG_NAME, "input")
    button.is_enabled()


def do_cards(driver: undetected_chromedriver.Chrome):
    driver.get("https://app.member.virginpulse.com/#/home")
    time.sleep(2)
    next_button = driver.find_elements(By.ID, "vpg-pagination-btn-forward-")[0]
    ids = ["//*[contains(text(), 'GOT IT!')]", "//*[contains(text(), 'True')]", "//*[contains(text(), 'Not Now')]"]
    found_element = None
    end = False
    time.sleep(0.5)
    while not end:
        if not next_button.is_enabled():
            end = True
        for tag_id in ids:
            try:
                found_element = driver.find_element(By.XPATH, tag_id)
            except selenium.common.NoSuchElementException:
                continue
        if found_element:
            found_element.click()
        else:
            next_button.click()
        time.sleep(1)


def track_habits(driver: undetected_chromedriver.Chrome):
    responses = {
        "minutes": "60",
        "enter duration in minutes": "60",
        "enter hours of sleep": "8",
        "enter number of steps": "30000",
    }

    driver.get("https://app.member.virginpulse.com/#/healthyhabits")
    time.sleep(5)

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
                       elem.accessible_name.lower() == "track it!" or elem.accessible_name.lower() == "yes"]

    # JS click after entry input
    for button in button_elements:
        driver.execute_script("arguments[0].click();", button)


def do_recipes(driver):
    link_from_rewards(driver, "Browse healthy recipes")

    driver.get("https://zipongo.com/recipes/category/all")

    time.sleep(2)
    driver.find_elements(By.CLASS_NAME, "ant-col")[0].click()  # click one first recipe
    heart_button = driver.find_elements(By.CLASS_NAME, "heart")[0]
    heart_button.click()
    time.sleep(1)
    heart_button.click()

    driver.find_elements(By.CLASS_NAME, "add-ingredients-to-gl-button")[0].click()
    driver.find_elements(By.CLASS_NAME, "grocery-list-add-modal-confirm-container")[0].click()
    trash_buttons = driver.find_elements(By.CLASS_NAME, "trash-icon-item")

    for button in trash_buttons:
        driver.execute_script("arguments[0].click();", button)


def do_journey(driver):
    pass


def do_rethink(driver):
    driver.find_elements(By.CLASS_NAME, "details-title")[0].click()
    time.sleep(360)
