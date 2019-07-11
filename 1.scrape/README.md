# Web scraping

This folder contains web scraping scripts to generate addtional features followed by a demonstration notebook of feature engineering:

1. SecurityTrails records: [`security_trails.py`](https://github.com/joy-wj/email-classification/blob/master/1.scrape/security_trails.py)
2. Wappalyzer records: [`wappalyzer.py`](https://github.com/joy-wj/email-classification/blob/master/1.scrape/wappalyzer.py)
3. Social Medial Links: [`social_scrape.py`](https://github.com/ValiMail/interns_domain_classification/blob/master/scrape/social_scrape.py)
4. Feature Engineering Demonstration notebook: [`feature-engineering.ipynb`](https://github.com/joy-wj/email-classification/blob/master/1.scrape/feature-engineering.ipynb)

## API Documentation Reference

* SecurityTrails API: https://docs.securitytrails.com/docs
* Wappalyzer(Lookup API): https://www.wappalyzer.com/docs/ap

## About the API

Here is a rough summary of the Web Scraping APIs, just to give an overview. The acutal speed may differ under different conditions of different running laptops/machines.

| __Summary__  | __SecurityTrails__  | __Wappalyzer__   |
|:-------:|:-------:|:------:|
| Quota| 200k queries/month  | 100k queries/month
| Multiprocess  | 20 concurrent | 20 concurrent
| Speed  | 5 hours/130k data | 6 hours/130k data

### API Key

:warning: For security concern, the API keys are stored in one single file called `config.py` __only in your local directory__.<br/>
__The API scraping scripts assume that the `config.py` file is stored in the same local directory as `security_trails.py` and `wappalyzer.py`__

## Data

The domain data csv file is stored in the google drive folder [Google Drive > Data Science > data](https://drive.google.com/drive/folders/1cEiKNfFSNhfcsXVjBqI-RywphjTMxKsE?usp=sharing) as:

```domain_130k.csv```

Make sure the domain column appears as the first column and has a header name. For example:

|   | __domain__   |
|:-------:|------:|
| 0  | assecosol.com|
| 1  | jewishexperience.org	|
| 2 | ssrefl.com |
| 3 | garverteam.com  |
| 4  |digitalinspiration.com |

The scraping script is going to generate additional features and concantenate them as a multitude of columns following the first column in the table. More details will be shown in the below sessions.

### Test Data

Due to the API quota constraint, we created some small-sized testing data in the Google Drive folder: [Google Drive > Data Science > data](https://drive.google.com/drive/folders/1eImejP0Yh5Wf0pd1PAfwiVDReUCgM45a), like `test_domain_100.csv`, with only 100 domains in the csv file to test the API scripts.

## [1. SecurityTrails](https://github.com/joy-wj/email-classification/blob/master/1.scrape/security_trails.py)

The goal of the `security_trails.py` script is to take a `.csv` file with a column of domains and generate associated security trails critical information. The column names to be generated are listed below:

* `WHOIS_counts`: num of WHOIS records
* `company_list`: a list of unique company names
* `company_name_counts`: num of unique company names
* `host_provider`: a list of unique host providers
* `host_provider_counts`: num of unique host providers
* `mail_provider`: a list of unique mail providers
* `mail_provider_counts`: num of unique mail providers
* `registrar`: a list of unique registrar names
* `registrar_counts`: num of unique registrar names called
* `security_trail_exist`: whether SecurityTrails records exist

To run the script, use the below command line

```bash
python security_trails.py file_path new_file_path
python scrape/security_trails.py data/test_domain_100.csv data/test_domain_100-results.csv
```

Note:

1. `file_path` is where the domain csv file stores, `new_file_path` is where the generated csv file going to be. You can put the two paths as the same one to update the original file.
2. The data files are not necessarily to be stored in the same directory as the script.

## [2. Wappalyzer](https://github.com/joy-wj/email-classification/blob/master/1.scrape/wappalyzer.py)

The goal of the `wappalyzer.py` script is to take a `.csv` file with a column of domains and generate associated web technology information. The column names to be generated are listed below:

* `app_list_exist`: whether Wapplayer records exist
* `category_list`: a list of unique categories
* `category_list_counts`: num of unique categories
* `web_tech`: a list of unique web technologies
* `web_tech_counts`: num of unique web technologies

To run the script, use the below command line

```bash
python wappalyzer.py file_path new_file_path
python scrape/wappalyzer.py data/test_domain_100.csv data/test_domain_100-results.csv
```

Note:

1. `file_path` is where the domain csv file stores, `new_file_path` is where the generated csv file going to be. You can put the two paths as the same one to update the original file.
2. The data files are not necessarily to be stored in the same directory as the script.

## [3. Social Media Links](https://github.com/joy-wj/email-classification/blob/master/1.scrape/social_scrape.py)

The goal of the `social_scrape.py` script is to take a `.csv` file with a column of domains and generate associated web technology information. The column names to be generated are listed below:

* `tld`: top level domain
* `linkedin`: whether LinkedIn links exist
* `facebook`: whether Facebook links exist
* `twitter`: whether Twitter links exist
* `youtube`: whether Youtube links exist
* `instagram`: whether Instagram links exist

To run the script, use the below command line

```bash
python social_scrape.py file_path output_path
```

Note:

1. `file_path` is where the domain csv file stores, `output_path` is where the generated csv file going to be. You can put the two paths as the same one to update the original file.
2. The data files are not necessarily to be stored in the same directory as the script.
3. The scraping script is using `multiprocessing` to perform scraping on multiple URLs simultaneously thus saving on time. The default number of multi-processor is 24 right now and you are free to change it in the script. However, the script is not necessarily running faster by setting more multi-processors.

## [4. Feature Engineering Demonstration](https://github.com/joy-wj/email-classification/blob/master/1.scrape/feature-engineering.ipynb)

The goal of the `feature-engineering.ipynb` is to demonstrate on Feature Engineering, which is how to create additional columns from API scraped records and scraped Social Media Links, specifically:

* How to clean the Social Media Links
* How to generate numeric and boolean columns from the below API scraped records:
    1. SecurityTrails: Raw content
    2. Wappalyzer: Raw content
* How to combine features into one dataset for model training

We took the 130k data as our example. Feel free to apply the scripts on other datasets(e.g. 40k, 46k etc) as well.
Make sure the data are saved in your local directory as:

```text
../data/domain_130k_API_records.csv
../data/domain_130k_social_links.csv.csv
../data/...
```

Next, we will be using the combined feature sets created from Feature Engineering process to build our classification models in the [model](https://github.com/joy-wj/email-classification/tree/master/2.model) session.
