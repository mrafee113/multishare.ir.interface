from selenium.webdriver.chrome.webdriver import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import Chrome
from settings import CREDENTIALS_PATH, CHROMEDRIVER_PATH, COOKIES_PATH
from settings import MainUrl

import os
import json
import configparser


def credentials():
    config = configparser.ConfigParser()
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError('credentials.ini not found')
    config.read('credentials.ini')

    return config.get('UserCredentials', 'username'), config.get('UserCredentials', 'password')


def webdriver(headless=False) -> WebDriver:
    options = Options()
    options.headless = headless

    driver = Chrome(CHROMEDRIVER_PATH, options=options)
    driver.set_window_rect(311, 142, 1550, 797)

    return driver


def login(driver: WebDriver):
    login_form_xpath = '//body//td[@class="cont-row"]//div[@class="block-bot"]//form[@id="user-login-form"]'
    el = driver.find_element_by_xpath(login_form_xpath)

    username, password = credentials()
    username_el = el.find_element_by_xpath('//input[@id="edit-name"]')
    username_el.send_keys(username)
    password_el = el.find_element_by_xpath('//input[@id="edit-pass"]')
    password_el.send_keys(password)

    el.submit()


def logout(driver: WebDriver):
    driver.get(f"{MainUrl}/main?log=logout")


def has_logged_in(driver: WebDriver):
    side_menu_xpath = '//body//td[@class="cont-row"]//div[@class="block-bot"]//div[@class="content"]'
    el = driver.find_element_by_xpath(side_menu_xpath)
    try:
        el.find_element_by_xpath('//ul[@class="menu"]')
    except NoSuchElementException:
        return False
    return True


def save_cookies(driver: WebDriver):
    with open(COOKIES_PATH, 'w') as file:
        json.dump(driver.get_cookies(), file, indent=8)


def load_cookies(driver: WebDriver):
    if not os.path.exists(COOKIES_PATH):
        return

    with open(COOKIES_PATH) as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()


def add_public_magnet(driver: WebDriver, magnet: str):
    xpath = '//body//td[@class="cont-row"]//div[@class="content"]//form[@id="searchform"]'
    el = driver.find_element_by_xpath(xpath)

    textarea = el.find_element_by_xpath('//textarea[@class="linkbox"]')
    textarea.send_keys(magnet)

    submit = el.find_element_by_xpath('//input[@class="w8-button l-blue"]')
    submit.submit()
