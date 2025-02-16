from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
import random
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

EMAIL = "sample@mail.com"
PASSWORD = "abcdef"
url = "https://www.naukri.com/nlogin/login"


class Config:
    SEARCH_BAR_XPATH = '//span[text() = "Search jobs here"]'
    JOB_TYPE_INPUT_XPATH = '//*[@id="jobType"]'
    JOB_OPTION_XPATH = (
        '//span[text() = "Job"]'  # require full time job and not internship
    )
    SKILL_INPUT_XPATH = (
        '//input[@placeholder = "Enter keyword / designation / companies"]'
    )
    FIRST_SKILL_OPTION_XPATH = '//li[contains(@class, "tuple-wrap")][1]'
    LOCATION_INPUT_XPATH = '//input[@placeholder = "Enter location"]'
    FIRST_LOCATION_OPTIONS_XPATH = FIRST_SKILL_OPTION_XPATH
    SEARCH_BUTTON_XPATH = '//span[text() = "Search"]'


def get_text_from_element(element):
    element_dict = {}
    # Get the tag name
    tag_name = element.tag_name
    # Get the text of the element itself
    element_text = element.text.strip()

    # Store the text in the dictionary with the tag name as the key
    element_dict[tag_name] = element_text

    # Get all child elements of the current element
    children = element.find_elements(By.XPATH, "./*")

    # Recursively add child elements' text
    if children:
        child_dict = []
        for child in children:
            child_dict.append(get_text_from_element(child))
        element_dict["children"] = child_dict

    return element_dict


class Naukri:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=options)
        self.application_logs = []

    def load_page(self, url):
        try:
            self.driver.get(url=url)
        except Exception as e:
            print(f"unable to load Page:{url}:{e}")

    def login(self):

        email_input = self.driver.find_element(By.ID, "usernameField")
        password_input = self.driver.find_element(By.ID, "passwordField")
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)
        login_button = self.driver.find_element(
            By.XPATH, '//*[@id="loginForm"]/div[2]/div[3]/div/button[1]'
        )
        login_button.click()

    def get_element(self, type, value):
        found_element = self.driver.find_element(type, value=value)
        if not found_element:
            print(f"Element not found:{value}")
        return found_element

    def select_job_type(self):
        job_type_input = self.get_element(By.XPATH, Config.JOB_TYPE_INPUT_XPATH)
        job_type_input.click()
        time.sleep(1)
        full_time_job_option = self.get_element(By.XPATH, Config.JOB_OPTION_XPATH)
        full_time_job_option.click()
        time.sleep(2)

    def enter_skills(self, skills):
        element = self.get_element(By.XPATH, Config.SKILL_INPUT_XPATH)
        element.click()
        for skill in skills:
            element.send_keys(skill)
            time.sleep(2)
            option = self.get_element(By.XPATH, Config.FIRST_SKILL_OPTION_XPATH)
            time.sleep(2)
            option.click()
            time.sleep(2)

    def enter_locations(self, locations):
        element = self.get_element(
            By.XPATH,
            Config.LOCATION_INPUT_XPATH,
        )
        element.click()
        for location in locations:
            element.send_keys(location)
            time.sleep(2)
            option = self.get_element(By.XPATH, Config.FIRST_LOCATION_OPTIONS_XPATH)
            time.sleep(2)
            option.click()
            time.sleep(2)

    def search(self):
        search_bar = self.get_element(By.XPATH, Config.SEARCH_BAR_XPATH)
        search_bar.click()
        time.sleep(5)

        self.select_job_type()
        self.enter_skills(
            ["python", "javascript", "software engineer", "fullstack developer"]
        )
        self.enter_locations(["chennai"])

        search_button = self.get_element(By.XPATH, Config.SEARCH_BUTTON_XPATH)
        search_button.click()

    def choose_freshness(self):
        self.get_element(By.XPATH, '//button[@title="Select"]').click()
        time.sleep(2)
        self.get_element(By.XPATH, '//span[text()="Last 3 days"]').click()
        time.sleep(3)
YXzOq9ryVc7!j@
    def choose_experience(self):
        element = self.get_element(By.XPATH, '//div[@class="handle"]')
        actions = ActionChains(self.driver)

        # Perform the drag and move action (2 pixels right)
        actions.click_and_hold(element).move_by_offset(5, 0).release().perform()
        time.sleep(3)

    def click_all_jobs(self):
        jobs = self.driver.find_elements(
            By.XPATH, '//div[@class="srp-jobtuple-wrapper"]'
        )

        for job in jobs:
            job.click()
            time.sleep(4)

    def switch_page_and_apply(self):
        original_window = self.driver.current_window_handle
        windows = self.driver.window_handles
        other_tabs = [window for window in windows if window != original_window]
        for tab in other_tabs:
            self.driver.switch_to.window(tab)
            job_header = self.get_element(By.XPATH, '//section[@id="job_header"]')
            job_desc = self.get_element(
                By.XPATH, '//section[@class="styles_job-desc-container__txpYf"]'
            )
            self.application_logs.append(
                {
                    "job_header": get_text_from_element(job_header),
                    "job_desc": get_text_from_element(job_desc),
                }
            )

    def start(self):
        try:
            self.load_page(url="https://www.naukri.com/nlogin/login")
            time.sleep(3)
            self.login()
            time.sleep(5)
            self.search()
            time.sleep(5)
            try:
                self.choose_freshness()
            except:
                print("freshness")
            try:
                self.choose_experience()
            except:
                print("exper")
            try:
                self.click_all_jobs()
            except Exception as e:
                print("click", e)
            time.sleep(1000000)

        except Exception as e:
            print(e)
            # self.write_into_json()


instance = Naukri()
instance.start()
time_period_selector = '//button[@title="Select"]'
time_period_option = '//span[text()="Last {no of days} days"]'
exp_chooser_selector = '//div[@class="handle"]'  # move this 4 pixel right for 1 yoe
