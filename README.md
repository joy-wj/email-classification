# Email Classification Project
Workspace for the Data Science interns to work on the domain classification project.

There will be a few steps involved in the following folders:

0. [data](https://github.com/joy-wj/email-classification/tree/master/0.data): A directory required to store all the csv files in your local folder
1. [scrape](https://github.com/joy-wj/email-classification/tree/master/1.scrape): Web-scrape additional data given domain csv files
2. [model](https://github.com/joy-wj/email-classification/tree/master/2.model): Train models based on given DNS data and scraped data created from feature engineering
3. [distribution](https://github.com/joy-wj/email-classification/tree/master/3.distribution): Display Model results and performance comparisons and visualize distributions of features
4. [model_comparison](https://github.com/joy-wj/email-classification/tree/master/4.model_comparison): Compare Model performances with different data
5. [pipeline](https://github.com/joy-wj/email-classification/tree/master/5.pipeline): Combine modularized scripts into one run

For detailed steps, please enter the respective folders to continue to explore. Before that, make sure to set up the environment by following __the below instructions__. 

# Set up environment
### Homebrew  
If you do not have [Homebrew](https://brew.sh/) installed in your environment, please follow instructions [here](https://brew.sh/). Or do:
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
### Python3 
All the scripts in this repo assume to run under the environment of Python3, please install Python3 using `Homebrew`:
``` bash
brew install python3
```

### Jupyter Notebook 
Please follow instruction [here](https://jupyter.org/install) to install jupyter notebook in your enviroment.  
It is strongly recommended to install Python and Jupyter using the [Anaconda Distribution](https://www.anaconda.com/distribution/), which includes Python, the Jupyter Notebook, and other commonly used packages for scientific computing and data science.

### Other Packages 
Please run the below command line to install packages included in the requirements file [`requirements.txt`](https://github.com/joy-wj/email-classification/blob/master/requirements.txt).

```bash
pip install -r requirements.txt
```
## Safe-keeping the API Key
After you have cloned or downloaded the repository to your local directory, make sure that `config.py` file(required to run the API tools) is saved in both of the [scrape](https://github.com/joy-wj/email-classification/tree/master/1.scrape) and [pipeline](https://github.com/joy-wj/email-classification/tree/master/5.pipeline) folders in your local directory only. 

```
interns_domain_classification/scrape/config.py
interns_domain_classification/pipeline/config.py
```
Please avoid commiting the `config.py` file to the repo to keep the API key safe. 


## Potential Problems

After we have gone through training the models and building pipelines, there are still a few potential issues identified:

__Features__

- Overfitting
  - The boolean columns from DNS data are created as a very sparse matrix
- Multicollinearity
  - The numeric columns from the counts features are correlated <br/>
(e.g. columns of `category_list` and `web_tech_counts`, `host_provider_counts` and `mail_provider_counts` are highly correlated)
  
__Data__

- Unbalanced data may hugely affect the model performance, not able to predict the untrusted data. 
- Resamplying method is not effective in terms of improving model performance (Only reached 70+% for both labels)

__model__

- The ability of our best model (built from the 46k balanced data) is still giving high probability to untrusted domain for being trusted. (e.g. 0.94). The reason could be that the specific untrusted data is also having Wappalyzer scraped features such as `web_tech_counts`, result in having a good indicator. 
- Other models could also be expored other than Logistic Regression and Random Forest.

## Appendix
[Final Prensetation Deck](https://github.com/joy-wj/email-classification/blob/master/Final_Presentation_Slides.pdf)


### Thank you for exploring. Have Fun!
