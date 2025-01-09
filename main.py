from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import random

# Set up the WebDriver
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in PATH

# Navigate to MonkeyType
driver.get("https://monkeytype.com")

# Wait for the cookie consent banner and reject non-essential cookies
try:
    reject_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'reject non-essential')]"))
    )
    reject_button.click()
    print("Rejected non-essential cookies.")
except Exception as e:
    print(f"Cookie consent handling failed: {str(e)}")

# Function to check if the typing test has started
def typing_test_started(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, ".word.active").is_displayed()
    except:
        return False

# Wait for the typing area to be ready and the test to start
try:
    WebDriverWait(driver, 20).until(typing_test_started)
    print("Typing test is ready to start.")
except TimeoutException:
    print("Timed out waiting for the typing test to start.")
    driver.quit()
    exit()

def get_active_word():
    try:
        active_word = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".word.active"))
        )
        return active_word.text
    except:
        return None

def type_word(word):
    actions = ActionChains(driver)
    actions.send_keys(word + " ")
    actions.perform()
    time.sleep(random.uniform(0.0000001, 0.0000007))  # Small random delay between words

# Main typing loop
try:
    while True:
        active_word = get_active_word()
        if active_word:
            type_word(active_word)
        else:
            time.sleep(0.001)  # Short delay if no active word is found
except KeyboardInterrupt:
    print("Typing stopped by user.")

# Close the browser
driver.quit()