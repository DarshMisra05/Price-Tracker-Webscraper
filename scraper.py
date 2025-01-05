from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime as dt
import csv
import os
import schedule


def job():
    csv_file = "pricing_data.csv"

    # if the file does NOT exist or is empty
    if not os.path.isfile(csv_file):
        with open(csv_file, mode = 'w', newline= '') as file:
            writer = csv.writer(file)
            writer.writerow(['Date and Time', 'Price'])

    # Define the path to the ChromeDriver
    path = r'C:\Users\Shlok.Misra\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    service = Service(path)

    # Start the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        url = "https://www.amazon.com/One-Piece-Box-Set-Skypiea/dp/1421576066"
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Get the page source
        html = driver.page_source

        # Extract price
        whole_price = driver.find_element(By.CLASS_NAME, 'a-price-whole').text
        dec_price = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text
        price = f"{whole_price}.{dec_price}"

        # Append new data to CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dt.now().strftime("%Y-%m-%d"), price])
            print("Data appended successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule "job" every day at noon
schedule.every().day.at("12:00").do(job)

# Keep the script running to execute the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)