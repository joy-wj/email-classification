# Email Domain Classification

The goal of this project is to build a model to predict labels for unknown domains. 

The code assumes the csv data files are saved in the a parent-directory: `data` from the current folder.  
The actual data files are stored in the google drive folder: [Google Drive > Email Classification](https://drive.google.com/drive/folders/1cEiKNfFSNhfcsXVjBqI-RywphjTMxKsE?usp=sharing)

# [Model](https://github.com/joy-wj/email-classification/blob/master/2.model/model.ipynb)
This notebook shows how to combine data from below to trail our models

1. Combine data
    * `domain_130k_dns.csv`: 130k domains with DNS data
    * `domain_130k_features.csv`: 130k domains with scraped data plus the created features
2. Train models
    * Logistic Regression
    * Random Forest
    * Feature Importances
3. Make predictions
4. Save & Load Model files from local directory

## Results & Performances
For the two models we created below are the summary of their performances

__Logistic Regression Model: 96% f1-score__

<img src=imgs/lr_model.png width=500>

__Random Forest Model: 95% f1-score__

<img src=imgs/rf_model.png width=500>


## Decision Tree Visualization

The below decision tree visualization plot shows how our model makes prediction. The model converts all the boolean DNS records variables like `ns_exists` into 1/0. To be more specific, whenever the DNS record exists, the decision goes to the right hand side branch 

<img src=imgs/decisionTreeViz.png width=850>

## Feature importance with ranking
For this model, we listed the top 20 most important features that are come up with by the Random Forest model:
- No.1 feature: category_list_counts (0.0742)
- No.2 feature: web_tech_counts (0.0714)
- No.3 feature: whois_counts (0.0614)
- No.4 feature: ns_exists (0.0526)
- No.5 feature: host_provider_counts (0.0481)
- No.6 feature: mail_provider_counts (0.0428)
- No.7 feature: ns_amazon_route53 (0.0381)
- No.8 feature: mx_exists (0.0364)
- No.9 feature: ns_godaddy (0.0362)
- No.10 feature: company_name_counts (0.0355)
- No.11 feature: facebook (0.0351)
- No.12 feature: app_list_exist (0.0291)
- No.13 feature: registrar_counts (0.0291)
- No.14 feature: spf_ends_in_inappropriate_all (0.0268)
- No.15 feature: mx_internal (0.0209)
- No.16 feature: twitter (0.0208)
- No.17 feature: ns_network_solutions (0.0181)
- No.18 feature: instagram (0.0172)
- No.19 feature: spf_exists (0.0172)
- No.20 feature: mx_google (0.0168)

We will report on distribution for some of the boolean columns from the top 20 important features in the [distribution](https://github.com/joy-wj/email-classification/tree/master/3.distribution) session.


## Save & Load models

### Make directory in current folder to save our models
```
model_path = Path("./saved_models")
model_path.mkdir(parents=True, exist_ok=True)

lr_path = model_path/'LR_model.sav'
rf_path = model_path/'RF_model.sav'
```
### Save model to local directory
```
pickle.dump(lr, open(lr_path, 'wb'))
pickle.dump(rf, open(rf_path, 'wb'))
```
### Load the model from local directory
```
loaded_LR = pickle.load(open(lr_path, 'rb'))
loaded_RF = pickle.load(open(rf_path, 'rb'))
```
### Make predictions
```
pred = loaded_RF.predict_proba(X_test)
```

Check the notebook of [model](https://github.com/joy-wj/email-classification/blob/master/2.model/model.ipynb) for details

