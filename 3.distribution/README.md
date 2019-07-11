# [EDA & Distribution](https://github.com/ValiMail/interns_domain_classification/blob/master/distribution/EDA_Correlations_Distributions.ipynb) 

This notebook shows the EDA and report on distributions for for the below csv files:
* 130k domains with DNS and web scraped features data: [`domain_130k_dns_features.csv`](https://drive.google.com/drive/folders/1eImejP0Yh5Wf0pd1PAfwiVDReUCgM45a)

Please continue the journey in the [model_comparison](https://github.com/ValiMail/interns_domain_classification/tree/master/model_comparison) session after this. 

# Correlations on numeric columns

<img src=imgs/correlations.png width=600>

As we can see from the above chart, there columns correlated to each other. This could be a potential problem of multicollinearity.

- `company_name_counts`
- `host_provider_counts`
- `mail_provider_counts`
- `registrar_counts`
<br/>

- `category_list_counts`
- `web_tech_counts`

# Distribution for boolean columns

Feature: ns_exists  
<img src=imgs/ns_exists.png width=500>

Feature: ns_amazon_route53  
<img src=imgs/ns_amazon_route53.png width=500>

Feature: mx_exists  
<img src=imgs/mx_exists.png width=500>

Feature: ns_godaddy  
<img src=imgs/ns_godaddy.png width=500>

Feature: facebook  
<img src=imgs/facebook.png width=500>

Feature: app_list_exist  
<img src=imgs/app_list_exist.png width=500>

Feature: spf_ends_in_inappropriate_all  
<img src=imgs/spf_ends_in_inappropriate_all.png width=500>

Feature: mx_internal  
<img src=imgs/mx_internal.png width=500>

Feature: twitter  
<img src=imgs/twitter.png width=500>

Feature: ns_network_solutions  
<img src=imgs/ns_network_solutions.png width=500>

Feature: mx_exists  
<img src=imgs/mx_exists.png width=500>

Feature: instagram  
<img src=imgs/instagram.png width=500>

Feature: spf_exists  
<img src=imgs/spf_exists.png width=500>

Feature: mx_google  
<img src=imgs/mx_google.png width=500>
