from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup

import time
import csv

def init_driver(browser):
    if browser.lower() == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path='path/to/chromedriver', options=options)
    elif browser.lower() == 'firefox':
        driver = webdriver.Firefox(executable_path='path/to/geckodriver')
    else:
        raise ValueError('Unsupported browser')
    return driver


def scrape_listings(driver, url, num_pages):
    listings = []
    driver.get(url)

    for _ in range(num_pages):
        wait = WebDriverWait(driver, 10)
        time.sleep(5)  # Give the page time to load

        # Scrape listings data
        listing_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "c4mnd7m")]')))
        for listing in listing_elements:
            title = listing.find_element(By.XPATH,'.//span[contains(@class, "t6mzqp7")]').text
            price = listing.find_element(By.XPATH,'.//div[contains(@class, "pquyp1l")]').text
            link = listing.find_element(By.XPATH,'.//a[contains(@class, "l1j9v1wn")]').get_attribute('href')
            # rating = listing.find_element(By.XPATH, '//*[contains(@class, "r1dxllyb")][self::span or self::div]').text
            # rate_rev = listing.find_element(By.XPATH,'.//span[contains(@class, "r4a59j5")]').get_attribute('aria-label')
            # rate_rev = listing.find_element(By.XPATH, '//*[contains(@class, "r4a59j5")]').get_attribute('aria-label')
            # rating = ''
            # review = ''
            # if 'New' not in rate_rev:
            #     rating,review = rate_rev.split(',')
            #     rating = rating.replace(' out of 5 average rating','')
            #     review = review.replace('reviews','').replace(' ','')
            # elif 'New' in rate_rev:
            #     rating = 'New'
            #     review = 'New'
            #list_obj = {'title': title, 'price': price, 'link': link, 'rating': rating, 'review': review}
            list_obj = {'title': title, 'price': price, 'link': link}

            if list_obj in listings:
                continue
            else:
                listings.append(list_obj)

        # Go to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@aria-label, "Next")]')))
            next_button.click()
        except:
            break

    return listings


def save_to_csv(listings, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        #fieldnames = ['title', 'price', 'link', 'rating', 'review']
        fieldnames = ['title', 'price', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)
        print("Written to csv File")

# Define a function to scrape data from a property page
def scrape_property_data(driver, button_css_selector):
    wait = WebDriverWait(driver, 10)
    time.sleep(8)  # Give the page time to load

    # Click on the button to open the modal
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class,l1j9v1wn)]')))
    button.click()
    

    
    # Scrape data from the modal
    modal = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,_17itzz4)]')))
    modal_content = modal.find_element(By.XPATH,'//div[@class="_17itzz4"]//h3[@class="hghzvl1"]').text
    # modal_content = modal.find_elements_by_xpath('//div[@class="_17itzz4"]//h3[@class="hghzvl1"]')

    
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # modal_content = soup.find('div', {'class': '_1kb5zmd'}).get_text(strip=True)
    
    # Close the modal (assuming it has a close button with a specific CSS selector)
    #close_button = driver.find_element_by_css_selector('.l1j9v1wn')
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class,l1j9v1wn)]')))
    close_button.click()
    
    return modal_content

def scrape_houserules_data(driver):
    wait = WebDriverWait(driver, 10)
    time.sleep(2)  # Give the page time to load
    all_rules = []

    try:
        buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="l1j9v1wn b1k5q1b3 v18vkvko dir dir-ltr"]')))
        button = buttons[2]
        button.click()
        # Scrape data from the modal
        modal = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "cvgxlsq dir dir-ltr")]')))
        try:
            rules = modal.find_elements(By.XPATH,'//div[@class="t1rc5p4c dir dir-ltr"]')
            for rule in rules:
                all_rules.append(rule.text)
        finally:
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "l1j9v1wn czcfm7x dir dir-ltr") and contains(@aria-label, "Close")]')))
            close_button.click()
    except:
        all_rules = []

    return all_rules

def scrape_property_data_2(driver):
    wait = WebDriverWait(driver, 10)
    time.sleep(8)  # Give the page time to load
    print("finished loading details page")
    new_columns = {}
    rating_names = ['Cleanliness', 'Accuracy', 'Communication', 'Location', 'Check-in', 'Value']
    try:
        new_columns['rating'] = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "_17p6nbba")]'))).text
        new_columns['reviews'] = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "l1j9v1wn bbkw4bl c1rxa9od dir dir-ltr")]'))).text
        rating_categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_a3qxec")]')))

        for ratings in rating_categories:
            name = ratings.find_element(By.XPATH,'.//div[contains(@class, "_y1ba89")]').text
            rt = ratings.find_element(By.XPATH,'.//div[contains(@class, "_bgq2leu")]//span[contains(@class, "_4oybiu")]').text
            new_columns[f"rating_{name}"] = rt
            
    except:
        new_columns['rating'] = '-'
        new_columns['reviews'] = '-'
        new_columns.update({f"rating_{rating}": "-" for rating in rating_names})

    try:
        new_columns['superhost'] = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "_1mhorg9")]'))).text
    except:
        new_columns['superhost'] = '-'

    new_columns['house_rules'] = scrape_houserules_data(driver)
    return new_columns

def amenities_to_csv(driver):
    # Read the input CSV file
    input_file = 'airbnb_listings.csv'
    data = pd.read_csv(input_file)

    # Add a new column for scraped data
    #data['modal_content'] = ''

    # Modify the button_css_selector, modal-content-selector, and modal-close-button-selector with the appropriate values
    button_css_selector = '.l1j9v1wn'
    all_cols = {}
    # Scrape data for each URL and append it to the same row
    for index, row in data.iterrows():
        url = row['link']
        driver.get(url)
        #modal_content = scrape_property_data(driver, button_css_selector)
        new_columns = scrape_property_data_2(driver)
        for col, val in new_columns.items():
            if col in all_cols:
                all_cols[col].append(val)
            else:
                all_cols[col] = [val]
        #data.at[index, 'modal_content'] = modal_content

    # Overwrite the input CSV file with the updated data
    for col, val in all_cols.items():
        data[col] = val
    data.to_csv(input_file, index=False)

def main():
    # Set up the web driver
    browser = 'chrome'  # or 'firefox'
    driver = init_driver(browser)

    # Log in to Airbnb (replace with your own credentials or skip this step if not needed)
    # username = 'your_email@example.com'
    # password = 'your_password'
    # login_airbnb(driver, username, password)

    # Scrape listings
    url = 'https://www.airbnb.com/s/san-francisco/homes'  # Replace with your desired search URL
    #num_pages = 15  # Number of pages you want to scrape
    num_pages = 1
    listings = scrape_listings(driver, url, num_pages)

    # Save listings to CSV
    file_name = 'airbnb_listings.csv'
    save_to_csv(listings, file_name)

    amenities_to_csv(driver)

    # Close the web driver
    driver.quit()
    print("Done.")

if __name__ == '__main__':
    main()


