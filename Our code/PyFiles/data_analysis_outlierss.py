# -*- coding: utf-8 -*-
"""data_analysis_outliers.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Tr4me86cGGSAh71JEdU9CLRFJn8cAJFf
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install seaborn

# Commented out IPython magic to ensure Python compatibility.
# %pip install scikit-learn

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import sklearn


# Graphing numerical data for Mortality
def graphNumericData(df):
    num_data = df[['BMI', 'LESION_LEN_1', 'LESION_STENO_1', 'POSTOP_LOS', 'PROCEDUREID', 'TOTALPROCTIME']]
    for k in num_data:
        if k != 'MORTALITY_EVENT' or 'MI_EVENT' or 'STROKE_EVENT':
            plt.scatter(df[k],df['STROKE_EVENT']) ### Change the [_EVENT] to MI or STROKE when you want to look for them
            plt.title(k)
            plt.show()

# Ceating new dataframe for categorical data (excluding target variables)
def graphCatagData(df):
    cat_data = df [['ANESTHESIA','APPROACH','ASACLASS', 'COPD',
                'GENDER', 'HIGHRISK', 'HTN', 'INDICATION',
                'LESION_LOC_1', 'LESION_SIDE_1', 'LESION_TYPE_1',
                'NEUROCHANGE', 'POSTOP_COMPLICATIONS',
                'POSTOP_HEMABLEED', 'POSTOP_INFECT',
                'POSTOP_PSEUDOANEUR', 'PREOP_DIABETES',
                'PREOP_DIALYSIS', 'PREOP_DYSRHYTHMIA',
                'PREOP_SMOKING', 'PRIOR_BYPPVIENDAR',
                'PRIOR_CABG', 'PRIOR_CAD', 'PRIOR_CEACAS',
                'PRIOR_CHF', 'PRIOR_MAJAMP', 'PRIOR_PCI',
                'PRIOR_TIASTROKE', 'URGENCY']]
    # Charting catagorical distribution for in Mortality
    for k in cat_data:
        if k != 'MORTALITY_EVENT' or 'MI_EVENT' or 'STROKE_EVENT':
            df.groupby([k])['MORTALITY_EVENT'].mean().plot.bar() ### Change the [_EVENT] to MI or STROKE when you want to look for them
            plt.show()

# Setting the aesthetic style of the plots
def graphHistogram(df):
    sns.set_style("whitegrid")

    # Defining a function to create histograms and boxplots for specified columns
    def plot_histograms_boxplots(data, columns, dataset_name):
        fig, axes = plt.subplots(len(columns), 2, figsize=(12, 4 * len(columns)))
        for i, col in enumerate(columns):
            # Histogram
            sns.histplot(data[col], kde=True, ax=axes[i, 0])
            axes[i, 0].set_title(f'Histogram of {col} in {dataset_name}')
            # Boxplot
            sns.boxplot(x=data[col], ax=axes[i, 1])
            axes[i, 1].set_title(f'Boxplot of {col} in {dataset_name}')
        plt.tight_layout()

    # Columns of interest for both datasets
    columns_of_interest = ['BMI', 'LESION_LEN_1', 'LESION_STENO_1', 'POSTOP_LOS', 'PROCEDUREID', 'TOTALPROCTIME']

    # Plotting for Mathematics dataset
    plot_histograms_boxplots(df, columns_of_interest, 'Dataset')


# BMI is the only one with a normal distribution
# can scale down procedure_id with log, min/max scalar, or standard scalar

# Same boxplot as above, keeping for archive
# Box-plots for numerical to look for outliers in Mortality

def boxplotoutlier(df):
    num_data = df[['BMI', 'LESION_LEN_1', 'LESION_STENO_1', 'POSTOP_LOS', 'PROCEDUREID', 'TOTALPROCTIME']]
    for k in num_data:
        if k != 'MORTALITY_EVENT' or 'MI_EVENT' or 'STROKE_EVENT':
            sns.boxplot(df[k])
            plt.title(k)
            plt.show()

# SO MANY OUTLIERS WOW
# NEED FEATURE SCALING