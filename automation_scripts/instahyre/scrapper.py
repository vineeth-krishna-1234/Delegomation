import html2text
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By


def get_job_description(driver):
    try:
        job_description_div = driver.find_element(By.ID, "job-description")

        # Extract the inner HTML of the div
        job_description_html = job_description_div.get_attribute("innerHTML")

        # Convert HTML to Markdown
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False  # Include links in the Markdown
        markdown_text = markdown_converter.handle(job_description_html)
        return markdown_text
    except (
        NoSuchElementException,
        TimeoutException,
        ElementNotInteractableException,
        ElementClickInterceptedException,
    ) as e:
        return ""
    except Exception as e:
        print(e)
        return ""


def get_socials(driver):
    try:
        # Locate the <ul> element containing the social links
        social_links_ul = driver.find_element(By.CLASS_NAME, "new-social")

        # Find all <a> tags within the <ul>
        link_elements = social_links_ul.find_elements(By.TAG_NAME, "a")

        # Extract the href attributes (links) from the <a> tags
        links = [link.get_attribute("href") for link in link_elements]

        # Print the list of links
        return links

    except (
        NoSuchElementException,
        TimeoutException,
        ElementNotInteractableException,
        ElementClickInterceptedException,
    ) as e:
        return []
    except Exception as e:
        print(e)
        return []


def get_profile(driver):
    try:
        # Locate the profile heading div
        profile_heading = driver.find_element(By.CLASS_NAME, "profile-heading")
        job_role = company_name = location = experience = None

        try:
            job_role = profile_heading.find_element(By.TAG_NAME, "h1").text
        except Exception as e:
            print(e)

        try:
            company_name = profile_heading.find_element(
                By.CLASS_NAME, "company-name"
            ).text
        except Exception as e:
            print(e)

        try:
            location = profile_heading.find_element(
                By.CSS_SELECTOR, ".job-locations span"
            ).text
        except Exception as e:
            print(e)

        try:
            experience = profile_heading.find_element(
                By.CSS_SELECTOR, ".job-locations .experience"
            ).text
        except Exception as e:
            print(e)

        return {
            "company_name": company_name,
            "experience": experience,
            "location": location,
            "role": job_role,
        }
    except Exception as e:
        print(e)
        return {
            "company_name": None,
            "experience": None,
            "location": None,
            "role": None,
        }


def aggregate_data(driver):

    return {
        **get_profile(driver=driver),
        "job_description": get_job_description(driver=driver),
        "links": get_socials(driver=driver),
    }
