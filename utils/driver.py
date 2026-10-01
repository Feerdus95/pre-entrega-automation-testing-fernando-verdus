from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)
