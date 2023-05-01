from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import pandas as pd
import json

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


def scrape_listings(driver, city, url, num_pages, listings_df):
    driver.get(url)
    total_listings = 0
    for _ in range(num_pages):
        wait = WebDriverWait(driver, 10)
        time.sleep(5)  # Give the page time to load
        # Scrape listings data
        listing_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "c4mnd7m")]')))
        for listing in listing_elements:
            new_listing = {}
            new_listing['city'] = city['city']
            new_listing['state'] = city['state']
            new_listing['coast'] = city['coast']
            new_listing['title'] = listing.find_element(By.XPATH,'.//span[contains(@class, "t6mzqp7")]').text
            new_listing['room_type'] = listing.find_element(By.XPATH,'.//div[contains(@class, "t1jojoys")]').text
            new_listing['price'] = listing.find_element(By.XPATH,'.//div[contains(@class, "pquyp1l")]').text
            new_listing['link'] = listing.find_element(By.XPATH,'.//a[contains(@class, "l1j9v1wn")]').get_attribute('href')
            listings_df = listings_df.append(new_listing, ignore_index=True)
            total_listings += 1

        # Go to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@aria-label, "Next")]')))
            next_button.click()
        except:
            break

    return listings_df, total_listings

def amentity_scraper(driver):
    amenity_details = {}
    amenity_available = []
    num_amenities = 0

    wait = WebDriverWait(driver, 10)

    try:
        button_parent = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"b9672i7 dir dir-ltr")]')))
        button_text = button_parent.find_element(By.XPATH,".//button[@class='l1j9v1wn b65jmrv v7aged4 dir dir-ltr']").text

        num_amenities = int(''.join(filter(str.isdigit, button_text)))
        amenity_details['num_of_amenities'] = num_amenities
    except:
        amenity_details['num_of_amenities'] = 0

    try:
        # wait for the modal to open
        amenities_modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-section-id,'AMENITIES_DEFAULT')]"))
        )

        # get all the lines inside the modal
        amenities_list = amenities_modal.find_elements(By.XPATH,".//div[@class='_19xnuo97']")

        # print each amenity line
        for amenity in amenities_list:
            amenity_available.append(amenity.text)
        amenity_details['available_amenities'] = amenity_available
    except:
        amenity_details['available_amenities'] = amenity_available

    return amenity_details

def infra_specs_scraper(driver):
    wait = WebDriverWait(driver, 10)
    infra_details = {}
    max_guests = 0
    num_rooms = 0
    num_beds = 0
    num_baths = 0

    overview_section = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@data-section-id,'OVERVIEW_DEFAULT')]")))
    overview_list = overview_section.find_elements(By.XPATH,".//li[@class='l7n4lsf dir dir-ltr']")

    try:
        max_guests = int(''.join(filter(str.isdigit, overview_list[0].text)))
        infra_details['max_guests'] = max_guests
    except:
        infra_details['max_guests'] = 0

    try:
        num_rooms = (1 if 'Studio' in overview_list[1].text else int(''.join(filter(str.isdigit, overview_list[1].text)))) if len(overview_list) > 1 else 0
        infra_details['num_rooms'] = num_rooms
    except:

        infra_details['num_rooms'] = 0

    try:
        num_beds = int(''.join(filter(str.isdigit, overview_list[2].text))) if len(overview_list) > 2 else 0
        infra_details['num_beds'] = num_beds
    except:
        infra_details['num_beds'] = 0

    try:
        num_baths = float(''.join(filter(str.isdigit, overview_list[3].text))) if len(overview_list) > 3 else 0
        infra_details['num_baths'] = num_baths
    except:
        infra_details['num_baths'] = 0


    return infra_details

def scrape_houserules_data(driver):
    wait = WebDriverWait(driver, 10)
    time.sleep(2)  # Give the page time to load
    all_rules = []
    def close_modal():
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "l1j9v1wn czcfm7x dir dir-ltr") and contains(@aria-label, "Close")]')))
        close_button.click()

    things_to_know_divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"c1e17v3g dir dir-ltr")]')))
    for things_div in things_to_know_divs:
        title = things_div.find_element(By.XPATH, './/h3[@class="hghzvl1 dir dir-ltr"]').text
        # Only go through the House rules modal
        if str(title).strip() != 'House rules':
            continue
        show_more_btn = things_div.find_element(By.XPATH, './/button[@class="l1j9v1wn b1k5q1b3 v18vkvko dir dir-ltr"]')
        show_more_btn.click()
        modal = wait.until(EC.presence_of_element_located((By.XPATH, './/div[contains(@class, "cvgxlsq dir dir-ltr")]')))
        try:
            rules = wait.until(EC.presence_of_all_elements_located((By.XPATH,'.//div[@class="t1rc5p4c dir dir-ltr"]')))
            for rule in rules:
                all_rules.append(rule.text)
        finally:
            close_modal()

    return all_rules

def review_ratings_host_scraper(driver):
    wait = WebDriverWait(driver, 10)
    rating_names = ['Cleanliness', 'Accuracy', 'Communication', 'Location', 'Check-in', 'Value']
    details = {}
    # Scrape the details available on page
    try:
        rating = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "_17p6nbba")]'))).text
        details['rating'] = str(rating).strip("·")
    except:
        details['rating'] = '-'

    try:
        rating_categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_a3qxec")]')))
        for ratings in rating_categories:
            name = ratings.find_element(By.XPATH,'.//div[contains(@class, "_y1ba89")]').text
            rt = ratings.find_element(By.XPATH,'.//div[contains(@class, "_bgq2leu")]//span[contains(@class, "_4oybiu")]').text
            details[f"rating_{name}"] = rt 
    except:
        details.update({f"rating_{rating}": "-" for rating in rating_names}) 

    try:
        reviews = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "l1j9v1wn bbkw4bl c1rxa9od dir dir-ltr")]'))).text
        details['reviews'] = int(''.join(filter(str.isdigit, reviews)))
    except:
        details['reviews'] = '-'

    try:
        details['superhost'] = '-'
        info_divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "_1mhorg9")]')))
        for div in info_divs:
            if str(div.text).strip() == 'Superhost':
                details['superhost'] = 'Superhost'
                break
    except:
        details['superhost'] = '-'

    return details

def scrape_details_page(driver, df_row):
    #time.sleep(5)  # Give the page time to load
    modified_row = df_row._asdict()

    # scrape the details available on page
    details = review_ratings_host_scraper(driver)
    modified_row.update(details)

    amenities = amentity_scraper(driver)
    modified_row.update(amenities)

    infra_specs = infra_specs_scraper(driver)
    modified_row.update(infra_specs)

    # scrape rules modal
    modified_row['house_rules'] = scrape_houserules_data(driver)

    return modified_row

def scrape_all_listing_urls(driver, city_df, output_file_name, failure_row_index=0):
    total_listings = city_df.shape[0]
    for row in city_df.itertuples():
        try:
            curr_url = row.link
            driver.get(curr_url)
            city_df.loc[row.Index] = scrape_details_page(driver, row)
            print("Finished scraping and saving listing", row.Index + 1, "/", total_listings)
        except Exception as e:
            # In case of failure, save all rows till now to csv and move to next row
            print(f"Something went wrong with listing {row.Index+1} in city {row.city}. Saving all rows to csv till now and moving on.")
            print("Exception:", e)
            save_to_csv(city_df, output_file_name, failure_row_index, row.Index)
            failure_row_index = (row.Index + 1)
            continue

    return city_df, failure_row_index

def save_to_csv(df, file_name, start_index=0, end_index=0):
    if end_index == 0:
        df.iloc[start_index:].to_csv(file_name, mode='a', index=False, header=False)
    else:
        df.iloc[start_index:end_index].to_csv(file_name, mode='a', index=False, header=False)

def main():
    # Set up the web driver
    browser = 'chrome'  # or 'firefox'
    driver = init_driver(browser)

    # Log in to Airbnb (replace with your own credentials or skip this step if not needed)
    # username = 'your_email@example.com'
    # password = 'your_password'
    # login_airbnb(driver, username, password)

    #create a dataframe to store listings
    df_columns = [
        'city', 'state', 'coast', 'title', 'price', 'link', 'room_type', 'max_guests', 'num_rooms', 'num_beds', 'num_baths', 
        'rating', 'reviews', 'rating_Cleanliness', 'rating_Accuracy', 'rating_Communication', 
        'rating_Location', 'rating_Check-in', 'rating_Value', 'superhost', 'house_rules', 'num_of_amenities', 'available_amenities'
    ]
    listings_df = pd.DataFrame(columns=df_columns)

    # Define different csv files for each coast
    output_files = { 
        'West': 'listings_west_coast.csv', 'East': 'listings_east_coast.csv', 
        'North': 'listings_north_coast.csv', 'South': 'listings_south_coast.csv',
        'Central': 'listings_central_coast.csv'
    }

    # Write header row to all csv files
    for _, file in output_files.items():
        listings_df.to_csv(file, index=False)

    # Get list of city urls to scrape
    cities = {}
    with open('cities_list.json') as f:
        cities = json.load(f)

    # In case we want to limit the number of cities we scrape, uncomment this and edit coasts_to_scrape as needed
    # coasts_to_scrape = ['West', 'East']
    # cities = [city for city in cities if city['coast'] in coasts_to_scrape]

    for city in cities:
        city_str = city['url_string']
        search_url = 'https://www.airbnb.com/s/' + city_str + '/homes'
        num_pages = 1
        failure_row_index = 0
        output_file = output_files[city['coast']]
        city_df = pd.DataFrame(columns=df_columns)

        start_time = time.time()
        city_df, num_listings = scrape_listings(driver, city, search_url, num_pages, city_df)
        print(f"Finished searching for {num_listings} listings in {city['city']}, {city['state']}!")
        city_df, failure_row_index = scrape_all_listing_urls(driver, city_df, output_file)
        print(f"Finished scraping all listings in {city['city']}, {city['state']}!")

        # Save listings to CSV
        print(f"Writing all listings for {city['city']} to csv...")
        save_to_csv(city_df, output_file, failure_row_index)
        print("--- %s seconds ---" % (time.time() - start_time))
        print()


    # Close the web driver
    driver.quit()
    print("Done.")

if __name__ == '__main__':
    main()


