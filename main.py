from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
import time

# Promised internet speeds
PROMISED_UP = 900
PROMISED_DOWN = 900
# Twitter credentials
X_USERNAME = "abc@gmail.com"
X_PASSWORD = "codese"
USERNAME = "Tpython"


class InternetSpeedTwitterBot():
    def __init__(self):
        self.driver = webdriver.Chrome()  # Initialize the Chrome webdriver
        self.get_upload = 0  # Variable to store the upload speed
        self.get_download = 0  # Variable to store the download speed

    def internet_speed(self):
        # Measure internet speed using Speedtest
        self.driver.get("https://www.speedtest.net/")  # Open Speedtest website
        time.sleep(5)  # Wait for the page to load
        start_button = self.driver.find_element(By.CSS_SELECTOR, '.start-button a')  # Locate the start button
        start_button.click()  # Click the start button
        print("start button pressed")

        try:
            time.sleep(60)  # Wait for the test to complete
            result_download = self.driver.find_element(By.CSS_SELECTOR,
                                                       'span[data-download-status-value]')  # Get download speed
            print(f"download speed {result_download.text}")
            result_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                     'span[data-upload-status-value]')  # Get upload speed
            print(f"upload speed {result_upload.text}")
            self.get_upload = float(result_upload.text)  # Convert upload speed to float
            self.get_download = float(result_download.text)  # Convert download speed to float

        except NoSuchElementException:
            print("no element found")  # Handle case where speed could not be found

    def twitter(self):
        # Log into Twitter and post the speed complaint
        self.driver.get("https://x.com/i/flow/login")  # Open Twitter login page
        time.sleep(3)  # Wait for the page to load

        username = self.driver.find_element(By.CSS_SELECTOR,
                                            'input[autocapitalize="sentences"]')  # Locate username input
        username.send_keys(USERNAME)  # Enter username
        time.sleep(2)

        next_button = self.driver.find_element(By.XPATH,
                                               "//button[@type='button' and contains(., 'Next')]")  # Locate next button
        next_button.click()  # Click the next button
        time.sleep(2)

        try:
            test_input = self.driver.find_element(By.CSS_SELECTOR,
                                                  "input[data-testid='ocfEnterTextTextInput']")  # Locate email input
            test_input.send_keys(X_USERNAME)  # Enter email
            test_next = self.driver.find_element(By.XPATH, "//button[.//span[text()='Next']]")  # Locate next button
            test_next.click()  # Click the next button
            time.sleep(2)
        except Exception as e:
            pass  # Handle exceptions during email entry

        password = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')  # Locate password input
        password.send_keys(X_PASSWORD)  # Enter password
        time.sleep(1)
        login_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Log in']]")  # Locate login button
        login_button.click()  # Click the login button
        time.sleep(2)

        # Prepare the tweet message
        message = (
            f"Hey Internet Provider, why is my internet speed {self.get_download} down/{self.get_upload} up when I "
            f"pay for {PROMISED_DOWN} down/{PROMISED_UP} up?")

        input_message = self.driver.find_element(By.XPATH,
                                                 "//div[@data-testid='tweetTextarea_0']")  # Locate tweet input
        input_message.send_keys(message)  # Enter the tweet message
        time.sleep(3)
        post_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Post']]")  # Locate post button
        post_button.click()  # Click the post button


# Create an instance of the bot and execute the speed test
bot = InternetSpeedTwitterBot()
bot.internet_speed()  # Measure internet speed
if bot.get_upload < PROMISED_UP or bot.get_download < PROMISED_DOWN:
    bot.twitter()  # Post complaint if speeds are below promised values
