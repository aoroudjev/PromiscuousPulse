import time
import undetected_chromedriver


def login(driver: undetected_chromedriver.Chrome, credentials: dict, first_login=False):
    driver.get('https://app.member.virginpulse.com/#/home')
    time.sleep(5)
    input_elements = [elem for elem in driver.find_elements(undetected_chromedriver.By.TAG_NAME, 'input') if
                      elem.accessible_name.lower() in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name.lower())])
    driver.find_element(undetected_chromedriver.By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(10)
    if driver.title != "Virgin Pulse - Home":
        raise ValueError


def do_assessment(driver: undetected_chromedriver.Chrome):
    driver.get("https://app.member.virginpulse.com/#/surveys-ui/surveys/47069/intro")
    driver.execute_script("arguments[0].click();", driver.find_element(undetected_chromedriver.By.CSS_SELECTOR,
                                                                       "button[id='survey-start-button']"))
    button = driver.find_element(undetected_chromedriver.By.TAG_NAME, "input")
    button.is_enabled()


def do_cards(driver: undetected_chromedriver.Chrome):
    driver.get("https://app.member.virginpulse.com/#/home")
    next_button = driver.find_element(undetected_chromedriver.By.ID, "vpg-pagination-btn-forward-")
    got_it_button = driver.find_element(undetected_chromedriver.By.ID, "CHANGE ME")
    got_it_button.click()
    time.sleep(0.5)
    while True:
        next_button.click()
        time.sleep(0.5)
        got_it_button = driver.find_element(undetected_chromedriver.By.ID, "CHANGE ME")
        got_it_button.click()
        time.sleep(0.5)
        if not next_button.is_enabled():
            break

def track_habits(driver: undetected_chromedriver.Chrome):
    responses = {
        "minutes": "60",
        "enter duration in minutes": "60",
        "enter hours of sleep": "8",
        "enter number of steps": "30000",
    }

    driver.get("https://app.member.virginpulse.com/#/healthyhabits")
    time.sleep(5)

    button_elements = [elem for elem in driver.find_elements(undetected_chromedriver.By.TAG_NAME, "button") if
                       elem.accessible_name.lower() == "yes"]
    for button in button_elements:
        driver.execute_script("arguments[0].click();", button)

    # Write out activity to display hidden items
    activity = [elem for elem in driver.find_elements(undetected_chromedriver.By.TAG_NAME, "input") if
                elem.accessible_name == "What activity did you do? Select an activity or start typing"]
    activity[0].send_keys("Badminton\ue007")

    input_elements = [elem for elem in driver.find_elements(undetected_chromedriver.By.TAG_NAME, "input")]
    for input_field in input_elements:
        if input_field.accessible_name.lower() in responses:
            input_field.send_keys(responses[str(input_field.accessible_name.lower())])

    time.sleep(2)

    button_elements = [elem for elem in driver.find_elements(undetected_chromedriver.By.TAG_NAME, "button") if
                       elem.accessible_name.lower() == "track it!"]

    # JS click after entry input
    for button in button_elements:
        driver.execute_script("arguments[0].click();", button)
