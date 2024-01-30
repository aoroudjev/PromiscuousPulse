import time

import selenium.common
import undetected_chromedriver as uc
from undetected_chromedriver import By
from tkinter import simpledialog


def login(driver: uc.Chrome, credentials: dict, first_login=False):
    driver.get('https://app.member.virginpulse.com/#/home')
    time.sleep(5)
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input') if
                      elem.accessible_name.lower() in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name.lower())])
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(10)

    if first_login:
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        conf_code = simpledialog.askstring("Conformation Code",
                                           "You will receive an email confirmation. Please input your code here.")
        driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(conf_code)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    if driver.title != "Virgin Pulse - Home":
        raise ValueError


def link_from_rewards(driver, link_text: str):
    driver.get("https://app.member.virginpulse.com/#/my-rewards/earn")
    time.sleep(7)
    driver.find_elements(By.LINK_TEXT, link_text)[0].click()
    time.sleep(5)


def do_assessment(driver: uc.Chrome):
    driver.get("https://app.member.virginpulse.com/#/surveys-ui/surveys/47069/intro")
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       "button[id='survey-start-button']"))
    button = driver.find_element(By.TAG_NAME, "input")
    button.is_enabled()


def do_cards(driver: uc.Chrome):
    ids = ["//*[contains(text(), 'GOT IT!')]",
           "//*[contains(text(), 'WILL DO!')]",
           "//*[contains(text(), 'True')]",
           "//*[contains(text(), 'Not Now')]"]

    driver.get("https://app.member.virginpulse.com/#/home")
    time.sleep(2)
    next_button = driver.find_element(By.ID, "vpg-pagination-btn-forward-")
    time.sleep(0.5)

    found_element = None
    end = False
    while not end:
        if not next_button.is_enabled():
            end = True
        for tag_id in ids:
            try:
                found_element = driver.find_element(By.XPATH, tag_id)
                time.sleep(0.2)
            except selenium.common.NoSuchElementException:
                continue
        if found_element:
            found_element.click()
            found_element = None
        next_button.click()
        time.sleep(1)


def track_habits(driver: uc.Chrome):
    responses = {
        "minutes": "60",
        "enter duration in minutes": "60",
        "enter hours of sleep": "8",
        "enter number of steps": "30000",
    }

    driver.get("https://app.member.virginpulse.com/#/healthyhabits")
    time.sleep(5)

    # Write out activity to display hidden items
    activity = driver.find_element(By.XPATH,
                                   "//*[contains(text(), 'What activity did you do? Select an activity or start "
                                   "typing')]")
    activity.send_keys("Badminton\ue007")

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
    time.sleep(2)
    heart_button = driver.find_elements(By.CLASS_NAME, "heart")[0]
    heart_button.click()
    time.sleep(0.5)
    heart_button.click()

    # Add recipe then remove all items
    driver.find_elements(By.CLASS_NAME, "add-ingredients-to-gl-button")[0].click()
    driver.find_elements(By.CLASS_NAME, "grocery-list-add-modal-confirm-container")[0].click()
    buttons = driver.find_elements(By.TAG_NAME, "Button")
    for button in buttons:
        if "ADD" in button.accessible_name:
            button.click()
            break

    trash_buttons = driver.find_elements(By.CLASS_NAME, "trash-icon-item")
    for button in trash_buttons:
        driver.execute_script("arguments[0].click();", button)


def do_journey(driver):
    driver.get("https://app.member.virginpulse.com/#/journeys")


def do_rethink(driver):
    link_from_rewards(driver, "Complete a RethinkCare session")

    # Remove survey pop-up if present
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Not now')]").click()
        time.sleep(3)
    except Exception as e:
        print(e)

    driver.find_element(By.CLASS_NAME, "details-title").click()
    time.sleep(360)
