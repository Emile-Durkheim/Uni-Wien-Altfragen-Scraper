from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from subprocess import CREATE_NO_WINDOW

data = {
    'q_num_123456': {
        'index': '1',
        'question': 'When did the second world war end in full commitment as according to the Paris Climate Accord of 1923? (2)',
        'answers': {
            '1945': False,
            '1955': False,
            '1939': True,
            '1946': True
        },
        'answer_order': ['1945', '1955', '1939', '1946']
    }
}

def get_selenium(browser: str):
    """Starts Selenium without console window """
    try:
        if browser == 'chrome':
            chrome_service = ChromeService('chromedriver')
            chrome_service.creationflags = CREATE_NO_WINDOW
            return webdriver.Chrome()

        elif browser == 'firefox':
            firefox_service = FirefoxService('geckodriver')
            firefox_service.creationflags = CREATE_NO_WINDOW
            return webdriver.Firefox()

        else:
            raise ValueError("str must read 'chrome' or 'firefox', not " + browser)
    except:
        raise Exception('Something with Selenium went wrong')


def scrape(driver, interface, data=data):
    inter = interface
    pass