# Data Dictionary

Please download all csv files here in the google drive folder. [Google Drive > Email Classification](https://drive.google.com/drive/folders/1cEiKNfFSNhfcsXVjBqI-RywphjTMxKsE?usp=sharing)<br/>
Save the csv files in this folder (`data`) in your local directory, which includes the below:

| __Data files__   |  __# of Data points__ | __Feature Definition__ |
|:------|:------|:------|
| `domain_40k_API_results.csv` | 40k | API records |
| `domain_40k_features.csv`| 40k | Scraped Features |
| `domain_40k_social_links.csv` | 40k | Social Media Links |
| `domain_40k.csv` | 40k | Domain only |
| `domain_46k_API_results.csv` | 46k | API records |
| `domain_46k_features.csv` | 46k | Scraped Features |
| `domain_46k_social_links.csv` | 46k | Social Media Links |
| `domain_46k.csv` | 46k | Domain only |
| `domain_130k_all.csv` | 130k | DNS + Scraped Features |
| `domain_130k_API_results.csv` | 130k | API records |
| `domain_130k_dns.csv` | 130k | DNS only |
| `domain_130k_features_dns.csv` | 130k | Scraped Features + DNS (Without Categorical Columns) |
| `domain_130k_features.csv` | 130k | Scraped Features |
| `domain_130k_social_links.csv` | 130k | Social Media Links |
| `domain_130k.csv` | 130k | Domain only |
| `test_combined.csv` | 130k | DNS + Scraped Features (Without Categorical Columns)|
| `test_domain_100.csv` | 100 | Domain only |
| `test_sample.csv` | 50 | Domain only |

*__API records__: SecurityTrails + Wappalyzer*<br/>
*__Scraped Features__: API records + Social Media Links + Additional Counts Features*  

## Snap shots

## domain_130k.csv

This csv file contains 130k domain data with two columns:

* __domains__: domain names
* __labels__: trusted, untrusted, pending

Below is a Snap shot of the data:

| __domain__   |  __label__ |
|------:|------:|
| propertygrams.com |  pending |
| tracyreal.estate	 | pending |
| assecosol.com | trusted |
| jewishexperience.org  | trusted |
| ssrefl.com  | trusted |

## domain_130k_API_records.csv

This csv file contains 130k domain data with extra two columns of API results:

* __security_trails__: list of list of SecurityTrails records
* __app_list__: list of lisf of Wappalyzer scraped records

Below is a Snap shot of the data:

| __domain__   |  __label__ | __security_trails__ | __app_list__ |
|------:|------:|------:|------:|
| assecosol.com | trusted | \[{'whois': {'registrar': 'Ascio Technologies, ... | NaN |
| jewishexperience.org | trusted | \[{'whois': {'registrar': 'Register.com, Inc.',... | \[\[\['SEO'], 'Yoast SEO'], \[\['Reverse Proxy', 'W... |
| ssrefl.com | trusted | NaN | \[\[\['Reverse Proxy', 'Web Servers'], 'Nginx'], ... |
| garverteam.com | trusted | NaN | \[\[\['Reverse Proxy', 'Web Servers'], 'Nginx'], ... |
| digitalinspiration.com | trusted | \[{'whois': {'registrar': 'Gandi SAS', 'expires...	| \[\[\['Analytics'], 'Google Analytics'], \[\['JavaS...|

## domain_130k_social_links.csv

This csv file contains 130k domain data with scraped social media links:

* __url__: The actual urls of the 130k domain data
* __tld__: Top Level Domain of the 130k domain data
* __linkedin__: Whether there is hyperlink of linkedin on the domain page
* __linkedin__: Whether there is hyperlink of linkedin on the domain page
* __facebook__: Whether there is hyperlink of facebook on the domain page
* __twitter__: Whether there is hyperlink of twitter on the domain page
* __youtube__: Whether there is hyperlink of youtube on the domain page
* __instagram__: Whether there is hyperlink of instagram on the domain page

Below is a Snap shot of the data:

| __url__   |  __tld__ | __linkedin__ | __facebook__ | __twitter__ | __youtube__ | __instagram__ |
|------:|------:|------:|------:|------:|------:|------:|
| https://www.propertygrams.com | com | N | Y | Y | N | N |
| https://www.tracyreal.estate | estate | N | N | N | N | N |
| https://www.assecosol.com | com | N | N | N | N | N |
| https://www.jewishexperience.org | org | N | Y | Y | Y | Y |
| https://www.ssrefl.com | com | N | N | N | N | N |
