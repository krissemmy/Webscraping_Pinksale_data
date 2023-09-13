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

    # If your chromedriver is in a different directory yo can uncomment line 29 and add the path to the chromedriver, also uncomment line 31 so that the service argument will be added
    #service = ChromeService(executable_path="/home/krissemmy/Downloads/chromedriver-linux64/chromedriver")

    driver = webdriver.Chrome(options=option)#, service=service)
    # driver = webdriver.Firefox()
    website = 'https://www.pinksale.finance/private-sales?chain=BSC'
    driver.get(website)
    driver.maximize_window()
    print("Hello World")
    time.sleep(10)

    fil = 2
    for f in ["kyc", "upcoming", "inprogress", "filled", "ended", "canceled"]:
        filter_c = driver.find_element(By.XPATH, '/html/body/div[1]/section/section/main/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[2]')
        filter_c.click()

        time.sleep(3)
        kyc = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div/div/div[2]/div[1]/div/div/div[{fil}]')
        kyc.click()
        fil += 1
        time.sleep(3)


        with open(f'{f}.csv','a',newline='') as file:
            count = 1
            condition = True
            scroll = 600
            filter = f
            while condition:
                try:
                    # Wait for an element to appear
                    wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds        /html/body/div[1]/section/section/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]
                    element = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/section/section/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[{count}]')))
                    time.sleep(5)
                    data = element.text
                    time.sleep(3)
                    t = data.split('\n')
                    if 'KYC' in t:
                        kyc_or_not = "Yes"
                    else:
                        kyc_or_not = "No"
                    time.sleep(1)

                    if len(t[-2]) >= 9:
                        presale = "Inprogress"
                    else:
                        presale = t[-2]
                    time.sleep(1)

                    coin_name = t[-10]
                    per_of_release = t[-9]
                    current_presale = t[-5].split(' ')[0]
                    soft = t[-7].split(' ')[0]
                    hard = t[-7].split(' ')[-2]
                    currency = t[-7].split(' ')[-1]
                    progress_percentage = t[-6].split('(')[-1].split(')')[0]
                    #If inprogress get the day hour minutes and seconds in format of %D:%H:%M:%S
                    day_hour_min_sec = t[-2]
                    # Get the current date
                    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    time.sleep(1)

                    file.write(f"{filter} ; {coin_name} ; {kyc_or_not} ; {presale} ; {per_of_release} ; {current_presale} ; {soft} ; {hard} ; {currency} ; {progress_percentage} ; {day_hour_min_sec} ; {current_date}\n")
                    count += 1
                    if count % 3 == 0:
                        # driver.scroll(0, 100)
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
                    condition = False
                    break


    time.sleep(50)
    driver.quit()

if __name__ == "__main__":
    get_pinksale_data()
    # column = ["filter", "coin_name", "kyc_or_not", "presale", "per_of_release", "current_presale", "soft", "hard", "currency", "progress_percentage", "day_hour_min_sec", 'current_date']
    # df4 = pd.read_csv("canceled.csv", delimiter = ";", names=column)
    # df.head()
