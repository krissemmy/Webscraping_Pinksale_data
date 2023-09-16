from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime


print("Hello")
def get_pinksale_data():
    """
    Scrape pinksale data based on filters
    """
    option = Options()

    # Add an option to disable website notifications
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    # Add an option to disable the "Chrome is being controlled by automated test software" notification
    option.add_argument("--disable-infobars")

    # If your chromedriver is in a different directory yo can uncomment line 27 and add the path to the chromedriver, also uncomment line 29 so that the service argument will be added
    #service = ChromeService(executable_path="/home/krissemmy/Downloads/chromedriver-linux64/chromedriver")

    driver = webdriver.Chrome(options=option)#, service=service)
    # driver = webdriver.Firefox()
    website = 'https://www.pinksale.finance/private-sales?chain=BSC'
    driver.get(website)
    driver.maximize_window()
    print("Hello World")
    time.sleep(10)

    with open('pinksale_data.csv','a',newline='') as file:
        i = 259
        condition = True
        scroll = 33800
        # scroll = 600
        filter = "Canceled"
        while condition:
            try:
                # Switch to the original tab
                driver.switch_to.window(driver.window_handles[0])
                # Wait for an element to appear (in this case, a button with id="myButton")
                wait = WebDriverWait(driver, 15)  # Wait up to 15 seconds   
                element = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/section/section/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[{i}]')))
                t = element.text.split('\n')
                current_presale = t[-5].split(' ')[0]
                file.write(f"{current_presale} ; ")

                time.sleep(3)
                # Find the button element you want to click   
                button = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/section/section/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[{i}]/div/div/div/div[5]/div/div[2]/a')))

                time.sleep(2)
                # Get the URL associated with the button
                button_url = button.get_attribute('href')

                time.sleep(2)
                # Execute JavaScript to open a new tab
                driver.execute_script("window.open('', '_blank');")

                time.sleep(1)
                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[1])

                time.sleep(2)
                # Navigate to the URL from the button in the new tab
                driver.get(button_url)
                time.sleep(2)
                
                driver.get(driver.current_url)
                time.sleep(5)
                
                # t = element.text.split('\n')
                data = driver.find_element(By.XPATH, '/html/body/div[1]/section/section/main/div[2]/div')
                data = data.text.split('\n')

                coin_name = data[0]

                if 'KYC' in data:
                    kyc_or_not = "Yes"
                else:
                    kyc_or_not = "No"

                if 'Audit' in data:
                    audit_or_not = "Yes"
                else:
                    audit_or_not = "No"

                description = max(data, key=len)
                # current_presale = t[-5].split(' ')[0]
                soft_cap = [s for s in data if 'Soft Cap' in s][0].split(' ')[-2]
                hard_cap = [s for s in data if 'Hard Cap' in s][0].split(' ')[-2]
                currency = [s for s in data if 'Maximum Buy' in s][0].split(' ')[-1]
                private_sale_start_time = [s for s in data if 'Private Sale Start Time' in s][0].split('Time ')[-1].split(' (')[0]
                private_sale_end_time = [s for s in data if 'Private Sale End Time' in s][0].split('Time ')[-1].split(' (')[0]
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                first_release_for_project = [s for s in data if 'First Release For Project' in s][0].split(' ')[-1]
                vesting_for_project = [s for s in data if 'Vesting For Project' in s][0].split('Project ')[-1]
                status = [s for s in data if 'Status' in s][0].split(' ')[-1]
                minimum_buy = [s for s in data if 'Minimum Buy' in s][0].split(' ')[-2]
                maximum_buy = [s for s in data if 'Maximum Buy' in s][0].split(' ')[-2]
                website = driver.find_element(By.XPATH, '/html/body/div[1]/section/section/main/div[2]/div/div[1]/div/div/article/div[2]/div/div[2]/div/a[1]')
                website_link = website.get_attribute('href')

                file.write(f"{coin_name} ; {kyc_or_not} ; {audit_or_not} ; {description} ; {soft_cap} ; {hard_cap} ; {currency} ; {private_sale_start_time} ; {private_sale_end_time} ; {current_date} ; {first_release_for_project} ; {vesting_for_project} ; {status} ; {minimum_buy} ; {maximum_buy} ; {website_link}\n")

                # Close the current tab (the new tab you switched to)
                driver.close()

                time.sleep(2)
                print(i)
                i += 1
                time.sleep(2)
                if i % 3 == 0:
                    # driver.scroll(0, 100)
                    driver.switch_to.window(driver.window_handles[0])
                    # Scroll down using JavaScript
                    print(scroll)
                    scroll_script = f"window.scrollTo(0, {scroll});"  # Adjust the values as needed
                    driver.execute_script(scroll_script)
                    scroll += 5
                    scroll_script = f"window.scrollTo(0, {scroll});"
                    driver.execute_script(scroll_script)
                    scroll += 410
            except:
                print(f"Error")
                # condition = False
                break


    time.sleep(50)
    driver.quit()

if __name__ == "__main__":
    get_pinksale_data()
    # column = [ 'current_presale',
    # 'coin_name',
    # 'kyc_or_not',
    # 'audit_or_not',
    # 'description',
    # 'soft_cap',
    # 'hard_cap',
    # 'currency',
    # 'private_sale_start_time_(UTC)',
    # 'private_sale_end_time_(UTC)',
    # 'date_last_updated',
    # 'first_release_for_project',
    # 'vesting_for_project',
    # 'status',
    # 'minimum_buy',
    # 'maximum_buy',
    # 'website_link']
    # df = pd.read_csv("pinksale_data.csv", delimiter = ";", names=column)
    # ordered_col = [ 'coin_name',
    # 'kyc_or_not',
    # 'audit_or_not',
    # 'description',
    # 'current_presale',
    # 'soft_cap',
    # 'hard_cap',
    # 'currency',
    # 'private_sale_start_time_(UTC)',
    # 'private_sale_end_time_(UTC)',
    # 'date_last_updated',
    # 'first_release_for_project',
    # 'vesting_for_project',
    # 'status',
    # 'minimum_buy',
    # 'maximum_buy',
    # 'website_link']
    # df = df[ordered_col]
    # df.head()
