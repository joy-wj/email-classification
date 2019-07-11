import sys
import config
import requests
import pandas as pd
from multiprocessing import Pool


def get_domains(file_path):
    """
    :param file_path: file path of the original domain csv
    :return: a DataFrame and a list of domains

    Given a domain csv file, the function read the csv into a DataFrame
    and return the DataFrame together with a list of the domains
    """
    df = pd.read_csv(file_path, low_memory=False)
    df = df.set_index(df.columns[0])
    domain_list = [domain for domain in df.index]
    return df, domain_list


def get_page_tech(domain):
    """
    :param domain: a single domain
    :return: list of list from the API scraped results

    Given a single domain and using the api_key from wappalyzer,
    scrape the page technology application information
    return the result in a list of list
    containing [[[category0], app0, app1...], [[category1], app0, app1...]]
    """

    api_key = config.wappalyzer_api_key

    headers = {"X-Api-Key": str(api_key)}
    print("begin", domain)
    r = requests.get(url="https://api.wappalyzer.com/lookup/v1/?url=https://"
                     + str(domain), headers=headers)
    results = r.json()
    if isinstance(results, list):
        latest_month = results[0]  # take the most recent month record
        app_list = latest_month['applications']
        if len(app_list) > 0:
            df_app = pd.DataFrame.from_dict(app_list)
            dict_app = df_app[['categories', 'name']].to_dict('split')
            return dict_app['data']


def get_len(val):
    """
    :param val: cell value as a list or as a set
    :return: length of the list or of the set
    """
    if isinstance(val, list) or isinstance(val, set):
        return len(val)
    else:
        return 0


def val_exists(val):
    """
    :param val: cell value as a list object
    :return: Boolean of whether the cell value contains Wappalyzer records
    """
    if val:
        return len(val) > 0
    else:
        return 0


def create_features(list_records, df):
    """
    :param list_records: list of records
    :param df: original domain DataFrame
    :return: a DataFrame with features created

    Given a list of API scraped records and the original DataFrame
    with the domains and Wappalyzer results
    create a multitude of features that contribute to our ML models,
    return a DataFrame object
    the columns include:

    1) 'app_list_exist': whether Wapplayer records exist
    2) 'category_list': a list of unique categories
    3) 'category_list_counts': num of unique categories
    4) 'web_tech': a list of unique web technologies
    5) 'web_tech_counts': num of unique web technologies
    """
    df = df.reset_index()
    df.loc[:, 'app_list'] = pd.Series(list_records)
    df.replace({'[]': None}, inplace=True)

    list_records = df['app_list']

    # init empty lists
    category_list = []
    web_tech_list = []

    for record in list_records:
        if record:
            table = pd.DataFrame(record)

            # init empty sets for:
            unique_category = set()
            unique_web_tech = set()
            
            # for category list
            for item in table[0]:
                if item:
                    category_name = set(item)
                    unique_category.update(category_name)
            category_list.append(unique_category)
            
            # for web technologies
            for item in table[1]:
                if item:
                    unique_web_tech.add(item)
            web_tech_list.append(unique_web_tech)

        else:
            category_list.append(None)
            web_tech_list.append(None)

    # 1)
    df['app_list_exist'] = df['app_list'].apply(val_exists).astype(int)

    # 2) & 3)
    df['category_list'] = pd.Series(category_list)
    df['category_list_counts'] = df['category_list'].apply(get_len).astype(int)

    # 4) & #5)
    df['web_tech'] = pd.Series(category_list)
    df['web_tech_counts'] = df['web_tech'].apply(get_len).astype(int)

    return df


if __name__ == '__main__':
    """
    launch the Python script file with the below command line:
    python wappalyzer.py file_path new_file_path
    """
    file_path = sys.argv[1]
    new_file_path = sys.argv[2]
    df, domains = get_domains(file_path)

    # create 20 concurrent running process in multiprocessing
    with Pool(20) as p:
        list_records = p.map(get_page_tech, domains)
    df_features = create_features(list_records, df)

    # save the DataFrame with features created into local file
    df_features.to_csv(new_file_path, index=False)
