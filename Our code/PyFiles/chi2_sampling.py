# -*- coding: utf-8 -*-
"""chi2_sampling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qwBxeEqDnWbZ2U5jceYw-Wncgyi4e_HN
"""

# Classification in Machine Learning: An Introduction - https://www.datacamp.com/blog/classification-machine-learning
# HIGHRISK should def have corellation with Stroke

# Commented out IPython magic to ensure Python compatibility.
# %pip install seaborn
# %pip install imblearn
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from scipy.stats import norm,chisquare
from sklearn.feature_selection import mutual_info_classif
import seaborn as sns
from sklearn.feature_selection import chi2
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest


def chisquare(df):
  columns_to_exclude = ['MORTALITY_EVENT', 'MI_EVENT', 'STROKE_EVENT', 'PROCEDUREID']
  X = df.drop(columns = columns_to_exclude)
  mortality_y = df['MORTALITY_EVENT']
  mi_y = df['MI_EVENT']
  stroke_y = df['STROKE_EVENT']

  rus = RandomUnderSampler(sampling_strategy=1)
  X_res_mi, y_res_mi = rus.fit_resample(X, mi_y)
  X_res_mortality, y_res_mortality = rus.fit_resample(X, mortality_y)
  X_res_stroke, y_res_stroke = rus.fit_resample(X, stroke_y)

  chi_mortality = chi2(X_res_mortality, y_res_mortality)
  chi_mi = chi2(X_res_mi, y_res_mi)
  chi_stroke = chi2(X_res_stroke, y_res_stroke)

  # Example scores and p-values from your chi-squared test
  # probably wouldve been easier to make a function lol
  mortality_scores = chi_mortality[0]
  mortality_p_values = chi_mortality[1]

  mi_scores = chi_mi[0]
  mi_p_values = chi_mi[1]

  stroke_scores = chi_stroke[0]
  stroke_p_values = chi_stroke[1]

  # Create a DataFrame for better visualization
  mortality_features_df = pd.DataFrame({'Feature': X_res_mortality.columns, 'Score': mortality_scores, 'p-value': mortality_p_values})
  mi_features_df = pd.DataFrame({'Feature': X_res_mi.columns, 'Score': mi_scores, 'p-value': mi_p_values})
  stroke_features_df = pd.DataFrame({'Feature': X_res_stroke.columns, 'Score': stroke_scores, 'p-value': stroke_p_values})

  # Set significance level
  alpha = 0.05

  # Filter for significant features
  mortality_significant_features = mortality_features_df[mortality_features_df['p-value'] < alpha]
  mi_significant_features = mi_features_df[mi_features_df['p-value'] < alpha]
  stroke_significant_features = stroke_features_df[stroke_features_df['p-value'] < alpha]

  # Optionally sort by score
  mortality_significant_features_sorted = mortality_significant_features.sort_values(by='Score', ascending=False)
  mi_significant_features_sorted = mi_significant_features.sort_values(by='Score', ascending=False)
  stroke_significant_features_sorted = stroke_significant_features.sort_values(by='Score', ascending=False)

  # Feed in top 5 variables
  print(mortality_significant_features_sorted)
  print("\n")
  print('-'*50)
  print("\n")
  # Mortality correlations

  print(mi_significant_features_sorted)
  print("\n")
  print('-'*50)
  print("\n")
  # MI correlations

  print(stroke_significant_features_sorted)
  print("\n")
  print('-'*50)
  print("\n")
  # stroke correlations

  # creates an empty list just to store the top 5 values for the adverse affects to index into later for the ML model
  Top5Stroke = []
  Top5Mortality = []
  Top5MI = []
  count = 0
  for x in stroke_significant_features_sorted.Feature:
    Top5Stroke.append(x)
    count = count + 1
    if count == 5:
      break
  count = 0
  for x in mortality_significant_features_sorted.Feature:
    Top5Mortality.append(x)
    count = count + 1
    if count == 5:
      break
  count = 0
  for x in mi_significant_features_sorted.Feature:
    Top5MI.append(x)
    count = count + 1
    if count == 5:
      break

  # example code of how you would go about using the top n lists as a filter to only get the df with the top n attributes
  # in this case n = 5
  MortalityX = df['MORTALITY_EVENT']
  MortalityY = df[Top5Mortality]

  return Top5Stroke, Top5Mortality, Top5MI,
