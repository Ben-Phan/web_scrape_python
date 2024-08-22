from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

def scrape_website():
    gecko_driver_path = 'C:/Users/benjamin.phan/Documents/Work/Sripts-Python/Python jen html/Samaya SEEL/geckodriver.exe'
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument('--ignore-ssl-errors')
    firefox_options.add_argument('--headless') # Enable this for headless mode, disable to open Chrome GUI

    driver = webdriver.Firefox(options=firefox_options)

    try:
        print("Accessing webpage")
        # Navigate to the webpage
        driver.get('https://erxxxxxxxxxx')
        print("Webpage loaded")

        # Find and fill in the user ID and password fields
        username = driver.find_element(By.NAME, 'XXUSER')
        username.send_keys('xxxxxx')

        password = driver.find_element(By.NAME, 'XXPSWD')
        password.send_keys('xxxxxxx')
        password.send_keys(Keys.RETURN)

        # Wait for the page to load after login
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be('https://erxxxxxxxx'))

        # Verification
        if driver.current_url == 'https://erxxxxxxx':
            print("Login successful.")
        else:
            raise Exception("Login failed or dashboard URL not loaded.")

        planning_schedules_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Planning Schedules')]")))
        planning_schedules_link.click()
        print("Clicked on Planning Schedules link")

        # Wait until the new page is loaded
        wait.until(EC.url_to_be('https://erxxxxx'))
        print("Opened page EZ006")

        # Click the view button to open the latest schedule
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'SelectionArrow')))
        form = driver.find_element(By.CLASS_NAME, 'SelectionArrow')
        view_button = form.find_element(By.XPATH, ".//input[@value='View']")
        view_button.click()

        # Wait for the schedule to load after clicking View
        time.sleep(30)

        # Wait until the schedule is visible
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'table')))

        # Get the HTML content
        html_content = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the 'Release Number' in the table
        release_number = None
        for td in soup.find_all('td'):
            if 'Release Number' in td.text:
                release_number_match = re.search(r'Release Number:(\d+)', td.text)
                if release_number_match:
                    release_number = release_number_match.group(1)
                    break

        if release_number is None:
            raise Exception("Release Number not found in the table.")

        # Create the filename with the release number
        filename = f"SA_{release_number}.htm"

        # Save the HTML content to a .htm file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML content saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    print("Starting program.")
    scrape_website()
    print("Program ended.")
