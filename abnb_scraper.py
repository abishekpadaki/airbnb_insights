from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

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
            title = listing.find_element(By.XPATH,'.//div[contains(@class, "t1jojoys")]').text
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
    num_pages = 15  # Number of pages you want to scrape
    listings = scrape_listings(driver, url, num_pages)

    # Save listings to CSV
    file_name = 'airbnb_listings.csv'
    save_to_csv(listings, file_name)

    # Close the web driver
    driver.quit()
    print("Done.")

if __name__ == '__main__':
    main()


