from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from claim_process import claim_process
import time


def go_to_login_page(driver):
    wait()
    # Wait for the element to be clickable
    login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/login/']")))

    # Click on the login link
    login_link.click()
    wait_page_load(driver)


def click_login_button(driver):
    # Find the login button by inner text and click it
    login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
    login_button.click()
    wait_page_load(driver)


def click_logout_button(driver):
    try:
        # Wait for the Logout element to be clickable
        logout_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log out')]"))
        )

        # Click the Logout element
        logout_element.click()
        wait_page_load(driver)
    except Exception as e:
        print("Error occurred while finding and clicking Log out element:", e)


def setup_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://yodayo.com/")
    driver.maximize_window()

    wait_page_load(driver)

    return driver


def wait_page_load(driver):
    # Wait until the page is fully loaded
    wait_time = 10
    WebDriverWait(driver, wait_time).until(
        lambda x: x.execute_script("return document.readyState == 'complete'")
    )


def wait(dur=3):
    # Increase the general wait time if your browser is giga slow.
    plus_waiting_time_you_want = 0

    time.sleep(dur + plus_waiting_time_you_want)


def find_and_tick_checkboxes(driver):
    try:
        # Find the button by inner
        enter_button = driver.find_element(By.XPATH, "//button[text()='Enter Yodayo']")
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

        if enter_button is not None:
            for checkbox in checkboxes:
                checkbox.click()

            enter_button.click()
        wait()
    except NoSuchElementException as e:
        print("Skipping checkboxes, either missing or unable to locate them.")


def fill_email_field(driver, credential_list, index):
    email_pos_in_list = 0
    email_field = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
    email_field.send_keys(credential_list[index][email_pos_in_list])


def fill_password_field(driver, credential_list, index):
    passw_pos_in_list = 1
    password_field = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    password_field.send_keys(credential_list[index][passw_pos_in_list])


def find_and_click_profile_picture(driver):
    try:
        # Wait for the profile picture element to be clickable
        wait()
        profile_picture = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Profile picture']"))
        )

        # Click on the profile picture
        profile_picture.click()

        wait_page_load(driver)
    except Exception as e:
        print("Error occurred while finding and clicking profile picture:", e)


def find_and_click_claim_yobeans(driver):
    try:
        # Wait for the Claim YoBeans link to be clickable
        claim_yobeans_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Claim YoBeans')]"))
        )

        # Click on the Claim YoBeans link
        claim_yobeans_link.click()
        wait_page_load(driver)
    except Exception as e:
        print("Error occurred while finding and clicking Claim YoBeans link.")


def claim_yo_beans(driver):
    try:
        claim_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Claim')]")

        # Execute JavaScript to click on the button
        driver.execute_script("arguments[0].click();", claim_button)
        wait_page_load(driver)
    except Exception as e:
        print("Error occurred while finding and clicking Claim button.")


def claim_loop(credential_list, stop_event):
    driver = setup_browser()

    for user in credential_list:
        if stop_event.is_set():
            break  # Exit the loop if stop event is set
        claim_process(driver, credential_list, credential_list.index(user))
        if stop_event.is_set():
            break  # Exit the loop if stop event is set

    driver.close()
