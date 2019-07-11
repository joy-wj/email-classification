# [Model Comparison](https://github.com/ValiMail/interns_domain_classification/blob/master/model_comparison/model_comparison.ipynb)

Although we have been able to get a 96% score in our [model](https://github.com/ValiMail/interns_domain_classification/tree/master/model) session, the model is based on highly unbalanced data, i.e. 90% of the label is `trusted`, 10% of the label is `untrusted`.   

In this session, we want to explore different model performances with both unbalanced and balanced data and apply additional Feature Engineering: __One-Hot Encoding__ to our data. See whether there is any performance increases.  

Again, all the `.csv` data files are stored in [Google Drive > Data Science > data](https://drive.google.com/drive/folders/1cEiKNfFSNhfcsXVjBqI-RywphjTMxKsE?usp=sharing). Below is a summary of the different datasets  we used to compare our model performances.

### Unbalanced vs Balanced data
| __Data files__   |  __# of Data points__ | __Features without DNS data__ |__Trusted - Untrusted Balance__| 
|:------|:------|:------|:------|
| `domain_40k_features.csv`| 40k | API records + Social Links | 90%-10% (Unbalanced) | 
| `domain_46k_features.csv` | 46k | API records + Social Links| 50%-50% (Balanced)| 
| `domain_130k_features.csv` | 130k | API records + Social Links | 90%-10% (Unbalanced)| 

## Methods
We adopted below approaches to solve the unbalanced situation and further improve our model.

- Resamplying
    - Downsamplying
    - Upsamplying
- One-Hot Encoding

### Resamlying 
We combine all our data to be __146k: 40k + 46k + 60k__  
_(Note that after removing the `pending` labels, the 130k data becomes 60k.)_

| __Label__ |__Data__| __Downsamplying__|__Upsamplying__|
|:------|:------|:------|:------|
| __trusted__ |116k| Resampled without replacement: 30k | Remains 116k |
| __untrusted__ |30k| Remains 30k | Resampled with replacement: 116k |

### One-Hot Encoding
One hot encoding is a process by which categorical variables are converted into a number of columns/features and append to the original DataFrame in order to improve the model performance. In particular, One-Hot Encoding does below to a DataFrame:

| __Categorical Col__ || __cat_1__| __cat_2__| __cat_3__| 
|:------:|:------:|:------:|:------:|:------:|
| cat_1 |-->| 1 | 0 | 0
| cat_2 |-->| 0 | 1| 0
| cat_3 |-->| 0 | 0| 1
| cat_2 |-->| 0 |1| 0
| cat_1 |-->| 1|0| 0
| cat_2 |-->|0| 1|0

In our case, we applied One-Hot Encoding to the categories of Top Level Domain in `tld` column. Although there are over 500 different categories in the top level domain, we don't want to append over 500 columns onto our DataFrame, which may cause the issue of overfitting and create a very sparse matrix.  

Instead, we get the top 30 categories that appear most in the `tld` column according to their occurrences by  `df['tld'].value_counts()` and create additional 31 columns (top 30 categories + 1 'other' for the rest) to append to the DataFrame. For this part, since we need to retain the same set of features/columns to create our prediction data columns, we will save the `tld_cat` list into a local file in the below folder:
```
../model/saved_model/tld_cat.txt
```
__For the demonstration of all the above methods, please refer to the actual code in: [`model_comparison.ipynb`](https://github.com/ValiMail/interns_domain_classification/blob/master/model_comparison/model_comparison.ipynb)__

## Comparison Results
### There are 6 sets of models created in total:
| __Datasets__ |__Balanced?__| __LR Model scores__|__RF Model scores__| 
|:------|:------|:------|:------|
| 40k |No| lr1 - trusted:0.96, untrusted:0 | rf1 - trusted:0.96, untrusted:0| 
| 46k |Yes| lr2 - trusted:0.89, untrusted:0.89 | rf2 - trusted:0.90, untrusted:0.90| 
| 60k |No| lr3 - trusted:0.95, untrusted:0 | rf3 - trusted:0.95, untrusted:0| 
| Down-sampled |Yes| lr4 - trusted:0.74, untrusted:0.76 | rf4 - trusted:0.74, untrusted:0.76| 
| Up-sampled |Yes| lr5 - trusted:0.74, untrusted:0.76 | rf5 - trusted:0.76, untrusted:0.79| 
| 46k + One-Hot Encoding |Yes| lr6 - trusted:0.91, untrusted:0.92 | rf6 - trusted:0.91, untrusted:0.92|

As you can see from the above table, Model set: `lr6` and `rf6` have the highest scores and are based on Balanced data. 
### Hence, we achieved a 92% score for a balanced model performance. This is without any DNS data involved. Yesh!

Then, we saved these best models(`lr6` and `rf6`) in the [saved_model](https://github.com/ValiMail/interns_domain_classification/tree/master/model/saved_models) folder as below.   

```
../model/saved_model/best_LR_model.sav
../model/saved_model/best_RF_model.sav
../model/saved_model/tld_cat.txt
```
Note: As mentioned earlier, the One-Hot Encoding Category list: `tld_cat` is saved as a `.txt` file. We will load it back in the script:[`one2one_predict.py`](https://github.com/ValiMail/interns_domain_classification/blob/master/pipeline/one2one_predict.py) in order to create the same set of Features(Columns) for our prediction data.   

Next, we will use these saved model files to build the [pipeline](https://github.com/ValiMail/interns_domain_classification/tree/master/pipeline) with predictions in one run.
