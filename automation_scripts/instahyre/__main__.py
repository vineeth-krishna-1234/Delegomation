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


class InstaHyre:

    def __init__(self, config):

        # Set up the Chrome options
        self.config = config
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.application_logs = []

    def load_page(self, url):
        try:
            self.driver.get(url=url)
        except Exception as e:
            print(f"unable to load Page:{url}:{e}")

    def login(self):

        self.load_page("https://www.instahyre.com/login/")
        self.sleep(5)
        email_input = self.get_element(By.NAME, "email")
        password_input = self.get_element(By.NAME, "password")
        email_input.send_keys(self.config.get("email"))
        password_input.send_keys(self.config.get("password"))

        login_button = self.get_element(
            By.XPATH, "//button[contains(@class, 'btn-success') and @type='submit']"
        )
        login_button.click()

    def get_element(self, type, value):
        return self.driver.find_element(type, value=value)

    def sleep(self, time_):
        time.sleep(time_)

    def enter_role(self):
        element = self.get_element(By.ID, "job-functions-selectized")
        self.wait.until(EC.element_to_be_clickable(element))
        element.click()
        for role in self.config.get("roles", []):
            element.send_keys(role)
            element.send_keys(Keys.ENTER)
            self.sleep(3)

    def enter_location(self):
        element = self.get_element(By.ID, "locations-selectized")
        self.wait.until(EC.element_to_be_clickable(element))
        element.click()
        for location in self.config.get("locations", []):
            element.send_keys(location)
            element.send_keys(Keys.ENTER)
            self.sleep(3)

    def enter_skill(self):
        element = self.get_element(By.ID, "skills-selectized")
        self.wait.until(EC.element_to_be_clickable(element))

        element.click()
        for skill in self.config.get("skills", []):
            element.send_keys(skill)
            element.send_keys(Keys.ENTER)
            self.sleep(3)

    def enter_experience(self):
        element = self.get_element(By.ID, "years")

        element.send_keys(self.config.get("experience", 0))
        self.sleep(3)

    def search(self):
        show_results_button = self.driver.find_element(By.ID, "show-results")
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", show_results_button
        )
        self.driver.execute_script("arguments[0].click();", show_results_button)

    def parse_company_details(self):

        application_details = {"company_info": "", "job_description": "", "urls": []}

        ## get summary
        company_info_element = self.get_element(By.CLASS_NAME, "company-info")
        application_details["company_info"] = company_info_element.text
        job_description_element = self.get_element(By.CLASS_NAME, "job-description")
        application_details["job_description"] = job_description_element.text
        link_parent_element = self.get_element(By.CLASS_NAME, "new-social")
        links = link_parent_element.find_elements(By.TAG_NAME, "a")
        all_urls = [link.get_attribute("href") for link in links]
        application_details["urls"] = all_urls
        return application_details

    def write_into_json(self):
        current_date = datetime.now()
        random_number = random.randint(100000, 999999)

        formatted_date = current_date.strftime("%d_%m_%Y")
        with open(
            f"applied_jobs/instahyre/{formatted_date}_{random_number}.json", "w"
        ) as json_file:
            json.dump(
                self.application_logs, json_file, indent=4
            )  # 'indent=4' formats the output with indentation

    def apply(self, limit=100):
        count = 0
        while count <= limit:
            try:
                # Click the "View more" button if it's present
                view_more_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "interested-btn"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", view_more_button
                )
                self.driver.execute_script("arguments[0].click();", view_more_button)

                # Step 5: Click the "Apply" button repeatedly
                apply_button = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "new-btn"))
                )
                self.application_logs.append(self.parse_company_details())
                apply_button.click()
                count += 1
                print(f"Applied to {count} jobs.")
                time.sleep(2)
            except (
                NoSuchElementException,
                TimeoutException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                print(e)
                print("No more jobs left to apply.")
            break

    def start(self):
        try:
            self.login()
            self.sleep(5)
            self.wait.until(
                EC.presence_of_element_located((By.ID, "job-functions-selectized"))
            )
            self.enter_role()
            self.enter_skill()
            self.enter_location()
            self.enter_experience()
            self.search()
            self.sleep(5)
            self.apply()
            self.write_into_json()
            self.driver.quit()
        except Exception as e:
            print(e)
            self.write_into_json()


config = {
    "email": "abc@gmail.com",
    "password": "secure password",
    "roles": ["backend", "frontend", "full"],
    "skills": ["python", "javascript"],
    "locations": ["Bangalore", "chennai", "coimbatore", "remote"],
    "experience": 1,
}

instance = InstaHyre(config=config)
instance.start()
