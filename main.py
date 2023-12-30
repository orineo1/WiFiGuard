import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def check_wifi_network(wifi_name):
    try:
        # Run the command to get the current Wi-Fi network name
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')

        # Check if "shori" or "shori_5" is in the output
        if wifi_name in result.lower() :
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def enter_to_tp_link(url, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)  # Use headless Chrome browser

    try:
        driver.get(url)
        time.sleep(2)
        # Find the password input field and enter the password
        password_input = driver.find_element(By.ID, "pc-login-password")
        password_input.send_keys(password)

        # Find the "Log In" button and click it
        login_button = driver.find_element(By.ID, 'pc-login-btn')
        login_button.click()

        # Wait for the next page to load
        wait = WebDriverWait(driver, 2)
        # Replace 'next-page-element-id' with an actual locator of an element on the next page

        # Check if there's a message about forcing other device to log off
        try:
            message = driver.find_element(By.CLASS_NAME, 'grid-warning-msg')
            if "Only one device can log in at a time." in message.text:
                confirm_button = driver.find_element(By.ID, 'confirm-yes')
                confirm_button.click()
        except:
            pass  # No message about forcing other device found

        # Perform further actions on the next page if needed

    except Exception as e:
        print(f"An error occurred: {e}")

    return driver
def check_connection_status(driver, status_element_id):
    try:
        # Find the status input field and get its value
        status_input = driver.find_element(By.ID, status_element_id)
        status_text = status_input.get_attribute('value')

        if "connected" in status_text.lower():
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred while checking status: {e}")
        return False

def reboot_device(driver):
    try:
        # Log the time when the reboot action is initiated
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open('reboot_log.txt', 'a') as log_file:
            log_file.write(f"\nReboot initiated at: {current_time}\n")

        # Find and click the "Reboot" button
        reboot_button = driver.find_element(By.ID, 'topReboot')
        reboot_button.click()

        # Wait for the message container to appear
        wait = WebDriverWait(driver, 3)
        message_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'position-center-right')))

        # Wait for the "Yes" button to be clickable within the message container
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#alert-container > div > div.position-center-left > div > div.msg-btn-container > div > div:nth-child(2) > button')))
        next_button.click()

        # Optionally, wait for the device to reboot and perform further actions if needed
        time.sleep(15)

        # Log the time when the reboot action is completed
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open('reboot_log.txt', 'a') as log_file:
            log_file.write(f"Reboot completed at: {current_time}\n")

    except Exception as e:
        print("not worked")
        print(f"An error occurred: {e}")

    driver.quit()
    return


def main (url,wifi_name,password):
    print("job started - Checking every 5 minutes")
    if check_wifi_network(wifi_name):
        driver = enter_to_tp_link(url, password)
        time.sleep(10)
        res = check_connection_status(driver, "internetStatus")
        if res is False:
            reboot_device(driver)
            print("Disconneted - start rebooting")

        print("Connected - finish the function")
    else:
        print("Not in the right wifi")

# Example usage:
url = 'http://192.168.1.1'
password = 'Aa12345!'
wifi_name = 'wifi_name'
main(url,wifi_name,password)
