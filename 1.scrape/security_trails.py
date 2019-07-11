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
    print("begin", domain)
    r = requests.get(url, headers=headers)
    trails_dict = r.json()
    key = 'records'
    if key in trails_dict:
        records = trails_dict[key]
        return records


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
    :return: Boolean of whether the cell value contains SecurityTrails records
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

    df = df.reset_index()
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


if __name__ == '__main__':
    """
    launch the Python script file with the below command line:
    python security_trails.py file_path new_file_path
    """
    file_path = sys.argv[1]
    new_file_path = sys.argv[2]
    df, domains = get_domains(file_path)

    # create 20 concurrent running process in multiprocessing
    with Pool(20) as p:
        list_records = p.map(get_security_trails, domains)

    df_features = create_features(list_records, df)

    # save the DataFrame with features created into local file
    df_features.to_csv(new_file_path, index=False)
