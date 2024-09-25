#This program ensures that the data attributes' cell values in the read-in .csv file are valid, according to the provided Data Dictionary.

import pandas as pd

df = pd.read_csv("Data for ML Model (v1).csv")

# Data should only contain numeric values.
# Convert non-numeric values to Nan
df = df.apply(pd.to_numeric, errors='coerce')


# Creates a filter for each value in the dataframe, where a valid value is "true" and a invalid value is "False."
# For ensuring that only certain values are in a column, the values specified in the Data Dictionary for the ML data as "Retired" are excluded.
#Horribly inefficent, I'm sure, but its simpler  to understand and doesn't need knowledge of another library to create.
conditions = {
    'ANESTHESIA' :df['ANESTHESIA'].isin([1,3,4,2]),
    'APPROACH' : df['APPROACH'].isin([1,4,5,3,6,7]),
    'ASACLASS' : df['ASACLASS'].isin([1,2,3,4,5]),

    #Ensures that 'BMI' is a positive, rational number. int & float are the only rational-number-only variable types in python (Year 2024). Approach also applied to other attributes.
    'BMI' : (df['BMI'] >= 0) & (df['BMI'].apply(lambda x: isinstance(x, (int, float)))),

    'COPD' : df['COPD'].isin([0,1,2,3]),
    'GENDER' :df['GENDER'].isin([1,2,99]),
    'HIGHRISK' :df['HIGHRISK'].isin([0,1,2,3]),
    'HTN' :df['HTN'].isin([0,2,3]),
    'INDICATION' :df['INDICATION'].isin([1,2,3]),
    'LESION_LEN_1' : df['LESION_LEN_1'].between(5,99),
    'LESION_LOC_1' :df['LESION_LOC_1'].isin([1,2,3,4]),
    'LESION_SIDE_1' :df['LESION_SIDE_1'].isin([1,2]),

    #Must be within values 0 to 100. Represents a percentage.
    'LESION_STENO_1' : df['LESION_STENO_1'].between(0,100),

    'LESION_TYPE_1' :df['LESION_TYPE_1'].isin([1,2,3,4,5,6,7,8]),

    'MI_EVENT' :df['MI_EVENT'].isin([0,1]),
    'MORTALITY_EVENT' :df['MORTALITY_EVENT'].isin([0,1]),

    'NEUROCHANGE' :df['NEUROCHANGE'].isin([0,2,3,4]),
    'POSTOP_COMPLICATIONS' :df['POSTOP_COMPLICATIONS'].isin([0,1]),
    'POSTOP_HEMABLEED' :df['POSTOP_HEMABLEED'].isin([0,1,2,3]),
    'POSTOP_INFECT' :df['POSTOP_INFECT'].isin([0,1,2]),

    #"POSTOP_LOS" must be a number. Ensures that 'POSTOP_LOS' is a positive, rational number. (Assumed to be true/needed) int & float are the only rational-number-only variable types in python (Year 2024). Approach also applied to other attributes.
    'POSTOP_LOS' :df['POSTOP_LOS'].apply(lambda x: isinstance(x, (int, float))),

    'POSTOP_PSEUDOANEUR' :df['POSTOP_PSEUDOANEUR'].isin([0,1,2,3,4]),
    'PREOP_DIABETES' :df['PREOP_DIABETES'].isin([0,1,2,3,4]),
    'PREOP_DIALYSIS' :df['PREOP_DIALYSIS'].isin([0,1,3,4]),
    'PREOP_DYSRHYTHMIA' :df['PREOP_DYSRHYTHMIA'].isin([0,5,2,3,4,6]),
    'PREOP_SMOKING' :df['PREOP_SMOKING'].isin([0,1,2]),
    'PRIOR_BYPPVIENDAR' :df['PRIOR_BYPPVIENDAR'].isin([0,1,2,3,4]),
    'PRIOR_CABG' :df['PRIOR_CABG'].isin([0,1,2]),
    'PRIOR_CAD' :df['PRIOR_CAD'].isin([0,6,1,2,4,5]),
    'PRIOR_CEACAS' :df['PRIOR_CEACAS'].isin([0,1,2,3]),
    'PRIOR_CHF' :df['PRIOR_CHF'].isin([0,1,2,3,4]),
    'PRIOR_MAJAMP' :df['PRIOR_MAJAMP'].isin([0,4,5,2,3]),
    'PRIOR_PCI' :df['PRIOR_PCI'].isin([0,1,2]),
    'PRIOR_TIASTROKE' :df['PRIOR_TIASTROKE'].isin([0,1]),

    #Unique ID for the procedure
    #Ensures that 'PROCEDUREID' is a positive, rational number. int & float are the only rational-number-only variable types in python (Year 2024). Approach also applied to other attributes.
    'PROCEDUREID' :df['PROCEDUREID'].apply(lambda x : (isinstance(x, (int, float)))),

    'STROKE_EVENT' :df['STROKE_EVENT'].isin([0,1]),

    #Description supplied by client:
    #Integer in minutes from access puncture/incision to closure
    #Min/max range: 10 to 500 minutes
    'TOTALPROCTIME' : df['TOTALPROCTIME'].between(10,500),
    'URGENCY' :df['URGENCY'].isin([1,2,3])
}

# Sets invalid values to Nan, which will be exported as empty cells in the .csv file.
for column, condition in conditions.items():
    df.loc[~condition, column] = pd.NA


# Write the resulting DataFrame to a new CSV file

df.to_csv('output7_csvFIltered.csv', index=False, na_rep='')