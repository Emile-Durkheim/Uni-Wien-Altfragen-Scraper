import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from subprocess import CREATE_NO_WINDOW
import __main__

data = {
    'q_num_123456': {
        'question': 'When did the second world war end in full commitment as according to the Paris Climate Accord of 1923? (2)',
        'answers': ['1945', '1955', '1967', '1939'],
        'is_selected': [False, False, True, True]
    }
}

data_order = []

def get_selenium(browser: str):
    """Starts Selenium without console window"""
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


def scrape(driver: webdriver.Firefox, inter, data=data):
    LOGIN_URL = '/login/'
    QUIZ_URL = '/mod/quiz/attempt'
    SUMMARY_URL = '/mod/quiz/summary'

    driver.get('https://moodle.univie.ac.at/')

    # Wait until exam page has been reached
    while LOGIN_URL in driver.current_url:
        inter.status('Warte auf Login...')
        time.sleep(0.5)

    while QUIZ_URL not in driver.current_url:
        inter.status('Warte auf Prüfung...')
        time.sleep(0.5)

    # Exam has been reached
    inter.status('Sammelt Altfragen...')

    while True:
        time.sleep(0.25)
        # Gathers questions and checks whether to add/update them
        questions = return_questions(driver)
        
        has_changes = False
        for id, question in questions.items():
            # Add to data and data_order if new item
            if id not in data_order:
                data_order.append(id)
                data[id] = question
                has_changes = True
            # Check if selection identical to last scan, else update
            elif data[id]['is_selected'] != question['is_selected']:
                data[id]['is_selected'] = question['is_selected']
                has_changes = True

        if has_changes:
            inter.print_data()

        # Checks if user has finished exam
        if SUMMARY_URL in driver.current_url:
            inter.finished()

        


def return_questions(driver: webdriver.Firefox):
    """
    Generates a dict with one key:value pair for each question on the page.
    Each key is the question's ID as taken from the site's HTML, and each the value is another dictionary
    containing the question's string, the answer's strings in a list, and bool values of whether the
    answer was selected in another list. 
    """
    questions = {}

    # Go over each question on the page
    q_elems = driver.find_elements('css selector', '.que')
    for q_elem in q_elems:
        # Set up the dictionary
        id = q_elem.get_attribute('id')
        question = questions[id] = {}
        
        # Fill the dictionary
        question['question'] = q_elem.find_element('class name', 'qtext').text
        question['answers'] = [a_elem.text for a_elem in q_elem.find_elements('css selector', '.flex-fill > p')]
        question['is_selected'] = [checkbox.is_selected() for checkbox in q_elem.find_elements('tag name', 'input[type=checkbox]')]

    return questions