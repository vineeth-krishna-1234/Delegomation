from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os


def get_driver():

    # Set the Chrome profile path dynamically
    chrome_profile_path = "/home/o_o/.config/google-chrome/Profile 1"

    chrome_options = Options()
    # Disable notifications
    chrome_prefs = {
        "profile.default_content_setting_values.notifications": 2,  # Block notifications
        "profile.default_content_setting_values.popups": 2,  # Block pop-ups
        "profile.default_content_settings.popups": 0,  # Ensure pop-ups are blocked
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # chrome_options.add_argument("--headless")  # comment for testing
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        f"user-data-dir={chrome_profile_path}"
    )  # Load user profile

    driver = webdriver.Chrome(options=chrome_options)

    return driver
