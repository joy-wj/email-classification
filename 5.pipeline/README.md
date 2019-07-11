# pipeline

In this session, there are three python scripts:

1. Prediction on domain without any features: [`one2one_predict.py`](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/one2one_predict.py)
2. Prediction on domain given features: [`predict.py`](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/predict.py)
3. A list of functions used: [`summary_fn.py`](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/summary_fn.py)

## [1. One to One Prediction](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/one2one_predict.py)

The goal of the `one2one_predict.py` script is to predict probability of a single domain being trusted.   
__input__: a single domain in string format, e.g. 'example.com'  
__output__: predicted probability of being trusted  

With below steps:
* Take the domain and use it to scrape features, including:
  * SecurityTrails
  * Wappalyzer
  * Social Media Links
  * 30 tld features generated from our Best Model
* Load model of `.sav` file from [saved_model](https://github.com/joy-wj/email-classification/tree/master/2.model/saved_models) folder, the loaded model is  pre-trained with the same set of features(columns) as the prediction script would produce. You can also load other the model in this script, refer to more detailed explanation in the following session (__Portable Models__)
* Make a prediction for the single data entry and generate a probability of it being `trusted`

### Portable models
Pre-trained models are saved in the [saved_model](https://github.com/joy-wj/email-classification/tree/master/2.model/saved_models) folder. 
```
../model/saved_model/best_LR_model.sav
../model/saved_model/best_RF_model.sav
...
```
You can always load other models with better performances to do the prediciton. There is only one thing to notice:  
:warning: **Make Sure to use the same set of features/columns in your Pre-trained model and your prediction data.**  
For instance, in our case, the feature set of the training set used to pre-train our best model and the feature set created in the one to one prediction script have to be exactly the same in order and in column types:
```
| API records |  Social Links | 31 tld columns |
(All converted to numeric column type and dropped the original categorical tld column)
```
In short, to replace the model in the pipeline, which may be trained from a different set of features, you will have to modify the funcitons of creating features in the [`summary_fn.py`](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/summary_fn.py) script. 

### API Key

For security concern, the API keys are stored in one single file called `config.py` __only in your local directory__. <br/>
:warning: __Please make sure that the same `config.py` file mentioned in [scrape](https://github.com/joy-wj/email-classification/tree/master/1.scrape) folder is stored in the same local directory as `one2one_predict.py`, in this case is your local [pipline](https://github.com/joy-wj/email-classification/tree/master/5.pipeline) folder.__

To run the script, please do below (e.g. `domain = 'example.com'`)

```bash
python one2one_predict.py 'example.com'
```


## [2. Prediction with existing data features](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/predict.py)

The goal of the `predict.py` script is to take a `.csv` file with a single column of domains and generate predictions based on our existing data columns available.

The script takes `test_sample.csv` as an example list of input domains and look up the domains in the assumed databse in order to extract matched data. The assumed database is a test file called `test_combined.csv`, which contains DNS, Scraped Features in Numeric and Boolean columns.

The two mentioned files are also from in the folder of [Google Drive > Email Classification](https://drive.google.com/drive/folders/1cEiKNfFSNhfcsXVjBqI-RywphjTMxKsE?usp=sharing) and should be saved in the local directory as below.

```text
../data/test_combine.csv
../data/test_sample.csv
```

The prediction column names are listed below:

* `domain`: domain name
* `trusted_proba`: the probability that this domain is trusted
* `prediction`: prediction label

To run the script, use the below command line

```bash
python predict.py input_path output_path
```

Note:

1. `file_path` is where the domain csv file stores, `output_path` is where the generated prediction csv file going to be.
2. The input domain namelist and output prediction files are not necessarily to be stored in the same directory as the script.

## [3. Summary Functions](https://github.com/joy-wj/email-classification/blob/master/5.pipeline/summary_fn.py)

The functions in this script are a combination of web-scraping and feature engineering. These functions are in support of the script `one2one_predict.py` mentioned in above.

* `get_df`: Given a input domain in string format, generate a DataFrame
* `get_len`: Given a cell value as a list or a set, get the length of the cell value
* `val_exists`: Given a cell value as a list, return whether this cell value exist
* `get_security_trails`: Given a single domain, get the SecurityTrails raw records using API key
* `get_page_tech`: Given a single domain, get the Wappalyzer raw records using API key
* `scrape`: Given a single domain, get a list of Boolean values whether social links exist
* `create_features_SecurityTrails`: Based on the SecurityTrails raw records, create numeric features
* `create_features_wappalyzer`: Based on the Wappalyzer raw records, create numeric features
* `create_features_social`: Based on the Social Media Links, create boonlean features
* `one_hot_enc`: Given a top level domain category list(`tld_cat`) and DataFrame, create one hot encoded features for additional 31 columns.

Note: the `tld_cat` list is generated in the [`model_comparison.ipynb`](https://github.com/joy-wj/email-classification/blob/master/4.model_comparison/model_comparison.ipynb) process from the best model and is also save in the [saved_model](https://github.com/joy-wj/email-classification/tree/master/2.model/saved_models) folder.

```text
../model/saved_model/tld_cat.txt
```
