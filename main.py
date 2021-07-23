# 🚀 This Project is in it's early stages of Development.
# 📌 Working on new features and main menu.
# ⚠️ Any Questions or Suggestions please Mail to: hendriksdevmail@gmail.com
# 🖥 Version: 0.1 Beta

import csv
import os
import platform
import random
import string
import subprocess
import sys
import warnings
import zipfile
from random import choice, uniform
from time import sleep

import requests
import undetected_chromedriver as uc
from fake_headers import Headers
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import (InvalidSessionIdException,
                                        NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha

import config
import auth
import proxy_config
from plugin_config import background_js, manifest_json


def clear():
    # clearing the screen
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')


clear()

print("Getting chromedriver")
print("Proxy: {}".format(config.use_proxy))
OSNAME = platform.system()

if OSNAME == 'Linux':
    OSNAME = 'lin'
    with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
        version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Darwin':
    OSNAME = 'mac'
    process = subprocess.Popen(
        ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
    version = process.communicate()[0].decode(
        'UTF-8').replace('Google Chrome', '').strip()
elif OSNAME == 'Windows':
    OSNAME = 'win'
    process = subprocess.Popen(
        ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
    )
    version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
else:
    print('{} OS is not supported.'.format(OSNAME))
    sys.exit()

major_version = version.split('.')[0]

uc.TARGET_VERSION = major_version

uc.install()


def type_me(element, text):
    """
    Type like a human
    """
    for letter in text:
        element.send_keys(letter)
        sleep(uniform(.1, .3))

options = webdriver.ChromeOptions()

if config.use_proxy == "true":
    proxy_split = proxy.split(":")
    PROXY_HOST = proxy_split[0]
    PROXY_PORT = proxy_split[1]
    PROXY_USER = proxy_split[2]
    PROXY_PASS = proxy_split[3]

    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js %
                    (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS))
    options.add_extension(pluginfile)

    print('Proxy: {}'.format(proxy))
else:
    pass

header = Headers(
    browser="chrome",
    os=OSNAME,
    headers=False
).generate()
agent = header['User-Agent']
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-web-security")
viewport = ['1920,1080']
options.add_argument(f"--window-size={choice(viewport)}")
options.add_argument("--log-level=3")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"user-agent={agent}")
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 40)

warnings.filterwarnings("ignore", category=DeprecationWarning)

url = 'https://twitter.com/login'



is_site_loading = True
site_loaded = 'success'

while(is_site_loading):
    try:
        driver.get(url)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        sleep(5)
        loading_yes = driver.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/main/div/div/div[1]/h1/span')
        is_site_loading = False

    except (NoSuchElementException, WebDriverException, InvalidSessionIdException) as e:
        site_loaded = 'false'
        is_site_loading = False

if site_loaded == 'success':

    # enter username
    user = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')))
    type_me(user, auth.username)

    # enter password
    first = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')))
    type_me(first, auth.password)

    # click login
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div'))).click()


    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/h2/span')))
        print("Login Sucess | Username: {}".format(auth.username))
    except (NoSuchElementException, WebDriverException, InvalidSessionIdException) as e:
        print("Login Failed | Username: {}".format(auth.username))

    sleep(10)
    driver.close()

else:
    print('\033[31m' + 'Trying next proxy...' + '\033[0m')
    os.remove('proxy_auth_plugin.zip')
