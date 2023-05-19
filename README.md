This is a final-project for the course CS267 called "Unearthing Hidden Insights from Airbnb Data Using Gradient-Boosted Decision Trees"

## Prerequisites/Installations

- Python 3.7+
- Selenium WebDriver
- Pandas (v 1.5.3 or lower for append to work)
- A modern web browser (Chrome or Firefox)
- Numpy
- Plotly
- Seaborn
- Matplotlib
- Xgboost
- Lightgbm
- Jupyter Notebook or any Python Notebook application

You can install all dependencies above by running `pip3 install -r Code/requirements.txt` Make sure you have pip installed to do this.

In case you are running this on a Apple MacOS machine, you might run into issues installing lightgbm.

To fix this follow the below steps:
1. Make sure homebrew is installed on you Mac
2. run `brew install gcc`
3. run brew install CMake`
4. run brew install lightgbm
5. Now finally you should be able to run the pip installations without errors.


# Part 1 - Airbnb Scraper

To run a demo of the scraper we have created `demo_scraper.py` in the folder Code/Demo_Scraper


This is a Python script for scraping Airbnb listing data. It uses Selenium WebDriver to interact with the website, load pages, and extract data. The extracted data includes details like city, state, coast, title, price, link, room type, max guests, number of rooms, beds, baths, ratings, number of reviews, superhost status, house rules, and amenities.

## NOTE: It is important to note that some functionalities of the scraper might fail if the Airbnb site has been updated.

## Setup of Scraper

1. Make sure you have Python 3.7+ installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

2. Install the required Python libraries using pip:

```bash
pip3 install selenium pandas
```

3. Download the appropriate WebDriver for your web browser:
   - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)
   
   Ensure the WebDriver executable is in your system's PATH, or adjust the `executable_path` argument in the `init_driver` function to point directly to your WebDriver executable.

## Usage of Scraper

1. To run the script, simply execute the following command in your terminal:

```bash
python Code/Demo_Scraper/demo_scraper.py
```

2. The script will start scraping Airbnb listings for only SF provided from the `Code/Demo_Scraper/sf.json` file.

3. The script generates CSV files with Airbnb listings for each coast (East, West, North, South, Central). The files will be named `listings_<coast_name>_coast.csv`. These files will be stored in the directory where you run the command.

4. If there is a failure during the scraping of a specific listing, the script will save all the previously scraped listings to the corresponding CSV file and move on to the next listing.

The execution should take around 3-5 mins to complete.

## The full scraper code that was used to create our large dataset of all 70 cities can be found in `Code/Scraper/abnb_scraper.py`

## Note
Web scraping is subject to the terms of use of the website being scraped. Airbnb's terms of service do not allow for web scraping on ceratin pages of their website, and we have ensured to respect their robot policies. 

# Datasets
After running our large scraper for 70 cities previously, we pre-processed and merged our datasets (that can be found in `Dataset/Scraped data`) into one csv file which is stored here in the `Dataset` folder as `model_ready_dataset.csv`

This dataset is used to run the EDA and train/test the models in the next section.

# Running the EDA and Model Python Notebooks

The two notebooks are in the folders `EDA` and `Models` within the `Code` folder, 

The first notebook is `EDA/airbnb_eda_notebook.ipynb` which was used to run our EDA processes.

The second notebook is `Models/airbnb_models_notebook.ipynb` which was used to train, test and compare our three models - XGBoost, LightGBM and a traditional Linear Regression model.

To run both the notebooks, open them using Jupyter notebook or a python notebook editor of your choice.

# Interactive Heatmap

An interactive heatmap, as demoed during the presentation, can be seen by opening the file `us_heatmap_with_tooltips.html` in the `Code` folder


# Github

This project has ben maintained on Github. You can visit the repository to view this readme file in a neat markdown UI.
https://github.com/abishekpadaki/airbnb_insights