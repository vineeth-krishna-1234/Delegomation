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
from datetime import datetime, timezone
import random
from automation_scripts.instahyre.scrapper import aggregate_data
from automation_scripts.common.db import MongoDBHandler
from automation_scripts.common.logger import get_logger


class InstaHyre:

    def __init__(self, config):

        # Set up the Chrome options
        self.config = config
        options = Options()
        chrome_profile_path = "/home/rick/.config/google-chrome/Profile 2"
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument(
            f"user-data-dir={chrome_profile_path}"
        )  # Load user profile

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.application_logs = []
        self.db_instance = MongoDBHandler()
        self.logger = get_logger()

    def load_page(self, url):
        try:
            self.driver.get(url=url)
        except Exception as e:
            self.logger.error(f"unable to load Page:{url}:{e}")

    def login(self):

        self.load_page("https://www.instahyre.com/login/")
        self.sleep(5)
        if "/candidate/opportunities/" in self.driver.current_url:
            self.logger.info("[Login]:already logged in")
            return
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
            self.sleep(1)
            element.send_keys(Keys.ARROW_DOWN)
            self.sleep(1)
            element.send_keys(Keys.ENTER)
            self.sleep(1)
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

    def apply(self):

        def click_view_more():
            try:
                view_more_button = self.driver.find_element(By.ID, "interested-btn")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", view_more_button
                )
                view_more_button.click()
                time.sleep(2)
                return True
            except (
                NoSuchElementException,
                TimeoutException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                return False
            except Exception as e:
                self.logger.error(f"[View Button]:{str(e)}")
                return False

        def click_apply_button():
            try:
                apply_buttons = self.driver.find_elements(
                    By.XPATH, "//button[contains(text(), 'Apply')]"
                )
                for apply_button in apply_buttons:
                    if apply_button.is_displayed():
                        job_details = aggregate_data(self.driver)
                        job_details = {**job_details, "url": self.driver.current_url}
                        # apply_button.click()
                        time.sleep(2)
                        return job_details
                return False

            except (
                NoSuchElementException,
                TimeoutException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                return False
            except Exception as e:
                self.logger.error(f"[Apply button]:{str(e)}")
                return False

        def click_next_button():
            try:
                next_button = self.driver.find_element(
                    By.XPATH, "//li[contains(text(), 'Next »')]"
                )
                if not next_button.is_displayed():
                    return False
                next_button.click()
                time.sleep(2)
                return True
            except (
                NoSuchElementException,
                TimeoutException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                return False
            except Exception as e:
                self.logger.error(f"[Next Button]:{str(e)}")
                return False

        while True:
            time.sleep(1)
            try:
                job_details = click_apply_button()
                if job_details:
                    # self.db_instance.insert_data(
                    #     collection_name="applications",
                    #     data={**job_details, "applied_at": datetime.now(timezone.utc)},
                    # )
                    print(job_details)
                    continue

                view_more = click_view_more()
                if view_more:
                    continue

                next_page = click_next_button()
                if not next_page:
                    break

            except (
                NoSuchElementException,
                TimeoutException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ) as e:
                break
            except Exception as e:
                self.logger.error(f"[Apply flow]:{str(e)}")

    def start(self):
        try:
            self.login()
            time.sleep(2)
            try:
                is_options_displayed = self.driver.find_element(
                    (By.ID, "job-functions-selectized")
                )
                if not is_options_displayed.is_displayed():
                    try:
                        job_search_heading = self.driver.find_element(
                            By.XPATH,
                            "//div[contains(@class, 'job-search-heading') and .//h6[text()='Search other jobs']]",
                        )
                        job_search_heading.click()
                    except Exception as e:
                        self.logger.error(f"[Job filter]:{str(e)}")
            except Exception as e:
                self.logger.error(f"[filter options]:{str(e)}")

            self.enter_role()
            self.enter_skill()
            self.enter_location()
            self.enter_experience()
            self.search()
            self.sleep(5)
            self.apply()
            self.driver.quit()
        except Exception as e:
            self.logger.error(f"[global error]:{str(e)}")


