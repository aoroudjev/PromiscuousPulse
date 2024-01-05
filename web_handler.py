import time

from undetected_chromedriver import By


def login(driver, credentials):
    driver.get('https://app.member.virginpulse.com/#/home')
    time.sleep(5)
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input') if
                      elem.accessible_name.lower() in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name.lower())])
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
