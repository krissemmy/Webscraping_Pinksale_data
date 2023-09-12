# PinkSale Data Scraper
## Overview
This Python script is designed to scrape data from the PinkSale Finance website's private sales section. It utilizes the Selenium library for web scraping and can be customized to filter data based on various criteria such as KYC status and sale status (upcoming, in progress, filled, ended, canceled).

## Prerequisites
Before running the script, ensure you have the following prerequisites installed:

1. Python 3.x
2. Selenium library (You can install it using pip install selenium)
3. ChromeDriver (Make sure it's compatible with your Chrome browser version)

## Usage
1. Clone this repository to your local machine.

2. Set up the ChromeDriver executable path:

- If your Chromedriver is in a different directory, you can uncomment line 29 and add the path to the Chromedriver.
- Also, uncomment line 31 so that the service argument will be added accordingly.
3. Open the script pinksale_scraper.py in a text editor.

4. Customize the script as needed:

- You can modify the website variable to specify the PinkSale Finance URL you want to scrape.
- Adjust the filters and criteria for data extraction according to your requirements.
5. Run the script using the following command:

```bash
python pinksale_scraper.py
```
6. The scraped data will be saved in CSV file's that matches the filter provided in the same directory as the script.

## Script Explanation
1. The script uses Selenium to automate a Chrome browser.
2. It navigates to the PinkSale Finance website and applies filters to select specific private sales.
3. Data is scraped and saved in a CSV file with relevant information, including KYC status, sale status, coin name, and more.
4. The script employs scrolling to load additional data.

## Disclaimer
This script is provided for educational purposes and personal use. Please be aware of the website's terms of service and use this script responsibly and in compliance with any applicable laws and regulations.

