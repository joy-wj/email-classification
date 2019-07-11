import sys
from pathlib import Path
import pickle
from summary_fn import *

if __name__ == '__main__':

    # take the domain from terminal input
    domain = sys.argv[1]

    df = get_df(domain)

    st_records = [get_security_trails(domain)]
    df_features = create_features_SecurityTrails(st_records, df)

    wap_records = [get_page_tech(domain)]
    df_features = create_features_wappalyzer(wap_records, df)

    social_records = scrape(domain)
    df_features = create_features_social(social_records, df)

    model_path = Path("../model/saved_models")

    tld_cat_path = model_path/'tld_cat.txt'
    df_features = one_hot_enc(tld_cat_path, df_features)

    df_use = df_features.select_dtypes(exclude='object')

    best_path = model_path/'best_RF_model.sav'
    loaded_RF = pickle.load(open(best_path, 'rb'))

    proba = loaded_RF.predict_proba(df_use)
    trusted_proba = proba[0][0]
    print("For domain:", domain, ", the predicted probability to be trusted is", round(trusted_proba, 3))
