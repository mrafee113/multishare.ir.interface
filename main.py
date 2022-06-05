from selenium.webdriver.chrome.webdriver import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import Chrome
from settings import ROOT_DIR

import os
import configparser


def credentials():
    config = configparser.ConfigParser()
    if not os.path.exists(os.path.join(ROOT_DIR, 'credentials.ini')):
        raise FileNotFoundError('credentials.ini not found')
    config.read('credentials.ini')

    return config.get('UserCredentials', 'username'), config.get('UserCredentials', 'password')


def webdriver(headless=False) -> WebDriver:
    options = Options()
    options.headless = headless

    driver = Chrome(os.path.join(ROOT_DIR, 'chromedriver'), options=options)
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
    driver.get(f"{ROOT_DIR}/main?log=logout")


def has_logged_in(driver: WebDriver):
    side_menu_xpath = '//body//td[@class="cont-row"]//div[@class="block-bot"]//div[@class="content"]'
    el = driver.find_element_by_xpath(side_menu_xpath)
    try:
        el.find_element_by_xpath('//ul[@class="menu"]')
    except NoSuchElementException:
        return False
    return True
