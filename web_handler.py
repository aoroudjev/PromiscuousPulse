import time

from undetected_chromedriver import By


def login(driver):
    driver.get('https://app.member.virginpulse.com/#/home')
    time.sleep(10)
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input')]
    print(len(input_elements))
    for i in input_elements:
        print(i.accessible_name)
