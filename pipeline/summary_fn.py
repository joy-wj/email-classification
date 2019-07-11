import config
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from tld import get_tld


def get_df(domain):
    """
    :param domain: input single domain in string format
    :return: a DataFrame with the first column named 'domain'
    """
    domain_list = [domain]
    domain_dict = {'domain': domain_list}
    df = pd.DataFrame(domain_dict)
    return df


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
    :return: Boolean of whether the cell value exists (contains SecurityTrails/Wappalyzer records)
    """
    if val:
        return len(val) > 0
    else:
        return 0


def get_security_trails(domain):
    """
    :param domain: a single domain
    :return: list of list from the API scraped results

    Given a single domain and the api_key from SecurityTrails,
    scrape the associated information about each of the domains
    that consume historical WHOIS records and company data
    return the result as a list of list
    """

    api_key = config.security_trails_api_key

    headers = {'Content-type': 'application/json'}
    url = 'https://api.securitytrails.com/v1/domain/' \
          + str(domain) + '/associated?apikey=' + str(api_key)
    print("begin scraping SecurityTrail with domain", domain)
    r = requests.get(url, headers=headers)
    trails_dict = r.json()
    key = 'records'
    if key in trails_dict:
        records = trails_dict[key]
        return records


def create_features_SecurityTrails(list_records, df):
    """
    :param list_records: list of records
    :param df: original domain DataFrame
    :return: a DataFrame with features created

    Given a list of API scraped records and the original DataFrame
    with the domains and SecurityTrails results
    create a multitude of features that contribute to our ML models,
    return a DataFrame object
    the columns include:

    1) 'WHOIS_counts': num of WHOIS records
    2) 'company_list': a list of unique company names
    3) 'company_name_counts': num of unique company names
    4) 'host_provider': a list of unique host providers
    5) 'host_provider_counts': num of unique host providers
    6) 'mail_provider': a list of unique mail providers
    7) 'mail_provider_counts': num of unique mail providers
    8) 'registrar': a list of unique registrar names
    9) 'registrar_counts': num of unique registrar names called
    10) 'security_trail_exist': whether SecurityTrails records exist
    """

    df.loc[:, 'security_trails'] = pd.Series(list_records)
    df.replace({'[]': None}, inplace=True)

    list_records = df['security_trails']

    # init empty lists
    company_list = []
    host_provider_list = []
    mail_provider_list = []
    registrar_list = []

    for record in list_records:
        if record:
            table = pd.DataFrame(record)

            # init empty sets for:
            unique_company_name = set()
            unique_host_provider = set()
            unique_mail_provider = set()
            unique_registrar = set()

            # For company name
            for item in table['computed']:
                company_name = item['company_name']
                if company_name:
                    company_name = company_name.lower()
                    if ',' in company_name:
                        # remove the postfix to avoid duplicates
                        company_name = company_name.split(',')[0]
                    unique_company_name.add(company_name)
            company_list.append(unique_company_name)

            # For host provider
            for item in table['host_provider']:
                if item:
                    host_provider = set(item)
                    unique_host_provider.update(host_provider)
            host_provider_list.append(unique_host_provider)

            # For mail provider
            for item in table['mail_provider']:
                if item:
                    mail_provider = set(item)
                    unique_mail_provider.update(mail_provider)
            mail_provider_list.append(unique_mail_provider)

            # For registrar
            for item in table['whois']:
                registrar = item['registrar']
                if registrar:
                    registrar = registrar.lower()
                    if ',' in registrar:
                        # remove the postfix to avoid duplicates
                        registrar = registrar.split(',')[0]
                    unique_registrar.add(registrar)
            registrar_list.append(unique_registrar)

        else:
            company_list.append(None)
            host_provider_list.append(None)
            mail_provider_list.append(None)
            registrar_list.append(None)

    # 1)
    df['whois_counts'] = df['security_trails'].apply(get_len).astype(int)

    # 2) & 3)
    df['company_name'] = pd.Series(company_list)
    df['company_name_counts'] = df['company_name'].apply(get_len).astype(int)

    # 4) & 5)
    df['host_provider'] = pd.Series(host_provider_list)
    df['host_provider_counts'] = df['host_provider'].apply(get_len).astype(int)

    # 6) & 7)
    df['mail_provider'] = pd.Series(mail_provider_list)
    df['mail_provider_counts'] = df['mail_provider'].apply(get_len).astype(int)

    # 8) & 9)
    df['registrar'] = pd.Series(registrar_list)
    df['registrar_counts'] = df['registrar'].apply(get_len).astype(int)

    # 10)
    df['security_trail_exist'] = df['security_trails'].apply(val_exists).astype(int)

    return df


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
    print("begin scraping wappalyzer with domain", domain)
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


def create_features_wappalyzer(list_records, df):
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


def scrape(domain):
    """
    :param url: url in string format
    :return: list of boolean values for its social media links
    """
    url = 'http://www.' + domain

    tld, l, f, t, y, i = "N", "N", "N", "N", "N", "N"

    try:
        tld = get_tld(url)
    except:
        pass

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="lxml")
    except:
        return [url, tld, l, f, t, y, i]

    try:
        l = soup.find('a', attrs={'href': re.compile("^https://www.linkedin.com")})['href']
        if l != 'N':
            l = 'Y'
    except:
        pass

    try:
        f = soup.find('a', attrs={'href': re.compile("^https://www.facebook.com")})['href']
        if f != 'N':
            f = 'Y'
    except:
        pass

    try:
        t = soup.find('a', attrs={'href': re.compile("^https://twitter.com")})['href']
        if t != 'N':
            t = 'Y'
    except:
        pass

    try:
        y = soup.find('a', attrs={'href': re.compile("^https://www.youtube.com")})['href']
        if y != 'N':
            y = 'Y'
    except:
        pass

    try:
        i = soup.find('a', attrs={'href': re.compile("^https://www.instagram.com")})['href']
        if i != 'N':
            i = 'Y'
    except:
        pass

    return [url, tld, l, f, t, y, i]


def create_features_social(social_records, df):
    """
    :param social_records: list of Boolean values indicated the social links exists
    :param df: DataFame created to store the features
    :return: the same DataFrame with newly created 5 columns
    """

    df['tld'] = pd.Series(social_records[1])
    df['linkedin'] = pd.Series(social_records[2]).astype('bool')
    df['facebook'] = pd.Series(social_records[3]).astype('bool')
    df['twitter'] = pd.Series(social_records[4]).astype('bool')
    df['youtube'] = pd.Series(social_records[5]).astype('bool')
    df['instagram'] = pd.Series(social_records[6]).astype('bool')

    return df


def one_hot_enc(tld_cat_path, df):
    """
    :param tld_cat_path: top level domain category file saved as .txt
    :param df: DataFrame to create one hot encoding
    :return: DataFrame with 30 more one hot features

    Given a list of tld categories saved from the same Training dataset
    of our Best Model, create a same set of columns for our prediction data
    """

    with open(tld_cat_path, 'r') as f:
        for item in f:
            tld_cat = list(item.split(','))

    df['tld_type'] = pd.Categorical(df['tld'], categories=tld_cat)
    df['tld_type'].fillna('other', inplace=True)
    tld_enc = pd.get_dummies(df['tld_type'])
    df = pd.concat([df, tld_enc], axis=1)
    df.drop(['tld_type'], axis=1, inplace=True)

    return df




