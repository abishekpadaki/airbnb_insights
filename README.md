# airbnb_insights

# Airbnb Scraper

This is a Python script for scraping Airbnb listing data. It uses Selenium WebDriver to interact with the website, load pages, and extract data. The extracted data includes details like city, state, coast, title, price, link, room type, max guests, number of rooms, beds, baths, ratings, number of reviews, superhost status, house rules, and amenities.

## Prerequisites

- Python 3.7+
- Selenium WebDriver
- Pandas
- A modern web browser (Chrome or Firefox)

## Setup

1. Make sure you have Python 3.7+ installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

2. Install the required Python libraries using pip:

```bash
pip install selenium pandas
```

3. Download the appropriate WebDriver for your web browser:
   - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)
   
   Ensure the WebDriver executable is in your system's PATH, or adjust the `executable_path` argument in the `init_driver` function to point directly to your WebDriver executable.

## Usage

1. To run the script, simply execute the following command in your terminal:

```bash
python airbnb_scraper.py
```

2. The script will start scraping Airbnb listings for different cities provided in the `cities_list.json` file.

3. The script generates CSV files with Airbnb listings for each coast (East, West, North, South, Central). The files will be named `listings_<coast_name>_coast.csv`.

4. If there is a failure during the scraping of a specific listing, the script will save all the previously scraped listings to the corresponding CSV file and move on to the next listing.

## Note

Web scraping is subject to the terms of use of the website being scraped. Airbnb's terms of service do not allow for web scraping without prior permission. This code is provided for educational purposes only, and users are responsible for how they choose to use it.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

Please make sure to update tests as appropriate. 

## License

[MIT](https://choosealicense.com/licenses/mit/)
