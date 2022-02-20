import logging
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import StaleElementReferenceException
from subprocess import CREATE_NO_WINDOW
from _data import data

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

    if not inter.tries_scraper_restart:  # This portion of code runs only at first startup
        driver.get(inter.exam_url)

        # Wait until exam page has been reached
        inter.status('Warte auf Login...')
        while LOGIN_URL in driver.current_url:
            time.sleep(0.5)

        inter.status('Warte auf Prüfung...')
        while QUIZ_URL not in driver.current_url:
            time.sleep(0.5)

        # Exam has been reached
        inter.exam_url = driver.current_url
        inter.status('Sammle Altfragen...')

    while True:
        time.sleep(0.25)

        # Gathers questions and checks whether to add/update them
        try:
            questions = return_questions(driver)
        except StaleElementReferenceException:  # Raised when page is switched in the middle of Selenium checking the page
            logging.info('No questions found on page')

        # Sorts gathered questions into data
        for id, question in questions.items():
            # Add to data and data_order if new item
            if id not in data['question_order']:
                data['question_order'].append(id)
                data[id] = question
                inter.print_data()
            # Check if selection identical to last scan, else update
            elif data[id]['is_selected'] != question['is_selected']:
                data[id]['is_selected'] = question['is_selected']
                inter.print_data()

        # Checks if user has finished exam
        if SUMMARY_URL in driver.current_url and inter.has_finished is False:
            inter.on_finish()


def return_questions(driver: webdriver.Firefox):
    """
    Generates a dict with one key:value pair for each question on the page.
    Each key is the question's ID as taken from the site's HTML, and each the value is another dictionary
    containing the question's string, the answer's strings in a list, and bool values of whether the
    answer was selected in another list. 
    """
    questions = {}

    # Go over each question on the page
    q_elems = driver.find_elements('class name', 'que')
    for q_elem in q_elems:
        # Set up the dictionary
        id = q_elem.get_attribute('id')
        question = questions[id] = {}
        
        # Fill the dictionary
        question['question'] = q_elem.find_element('class name', 'qtext').text
        question['answers'] = [a_elem.text for a_elem in q_elem.find_elements('class name', 'flex-fill')]
        question['is_selected'] = [checkbox.is_selected() for checkbox in q_elem.find_elements('tag name', 'input[type=checkbox]')]

        # If there's only a True and False answer option, answer text is saved under an element with class ml-1
        if question['answers'] == []:
            question['answers'] = [a_elem.text for a_elem in q_elem.find_elements('class name', 'ml-1')]

        # For when there's radio buttons instead of checkboxes
        if question['is_selected'] == []:
            question['is_selected'] = [radio_button.is_selected() for radio_button in q_elem.find_elements('tag name', 'input[type=radio]')]

    return questions