from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Define lists to store job data
job_names = []
job_descriptions = []
academic_levels = []
locations = []
salaries = []
professional_titles = []
experience_levels = []

try:
    # Navigate to the webpage
    driver.get('https://www.elempleo.com/co/ofertas-empleo/')

    # Optionally, wait for some time to let the page load completely
    time.sleep(5)

    # Close the cookie banner
    try:
        time.sleep(2)
        cookie_banner = driver.find_element(By.XPATH, '/html/body/div[10]/div/div[2]/a')
        cookie_banner.click()
    except (NoSuchElementException, ElementNotInteractableException):
        pass

    for i in range(1, 540):
        for j in range(1, 51):
            # Find elements containing job data
            job = driver.find_element(By.XPATH, f'/html/body/div[8]/div[3]/div[1]/div[3]/div[{j}]/div[1]/ul/li[1]/h2/a')
            driver.execute_script("arguments[0].scrollIntoView();", job)
            job.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            
            # Extract job data

            job_name = driver.find_element(By.XPATH, f'/html/body/div[7]/div[1]/div/div[1]/h1/span')
            job_description = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[1]/div[1]/div/p[1]/span')
            salary = driver.find_element(By.XPATH, f'/html/body/div[7]/div[1]/div/div[1]/div[2]/div[1]/p[1]/span/span[1]')
            academic_level = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[1]/div[2]/div[2]/div[1]/p[3]/span')
            location = driver.find_element(By.XPATH, f'/html/body/div[7]/div[1]/div/div[1]/div[2]/div[1]/p[2]/span/span/span[2]')
            experience_level = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[1]/div[2]/div[2]/div[2]/p[1]/span')
            professional_title = driver.find_element(By.XPATH, f'/html/body/div[7]/div[1]/div/div[1]/div[2]/div[2]/p[2]')
            try:
                more_prof_titles = professional_title.find_element(By.XPATH, f'/html/body/div[7]/div[1]/div/div[1]/div[2]/div[2]/p[2]/a')
                more_prof_titles.click()
                time.sleep(5)
                professional_titles_list = driver.find_element(By.XPATH, f'/html/body/div[1]/div[3]/div/div/div[2]/div/ul')
                titles = professional_titles_list.find_elements(By.TAG_NAME, 'li')
                for title in titles:
                    professional_titles.append(title.text)
            except NoSuchElementException:
                professional_titles.append(professional_title.text)
                
            job_names.append(job_name.text)
            job_descriptions.append(job_description.text)
            salaries.append(salary.text)
            academic_levels.append(academic_level.text)
            locations.append(location.text)
            experience_levels.append(experience_level.text)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
        time.sleep(5)
        print(f'Page {i} done')
        next_page = driver.find_element(By.XPATH, f'/html/body/div[8]/div[3]/div[1]/div[4]/div/nav/ul/li[8]/a')
        driver.execute_script("arguments[0].scrollIntoView();", next_page)
        next_page.click()
        time.sleep(10)
               
finally:
    # Close the browser
    driver.quit()