# -*- coding: utf-8 -*-
"""CSS145_BM3_Proposal2_Group6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b1sZBo6abbv3cw3z_CA6pVPB7Tn-aV0c

## Module Imports
"""

# Downloading Dataset from Kaggle
import kagglehub
import os

# Data Analysis
import pandas as pd
import numpy as np

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import plot_tree
from sklearn.utils import resample

"""## Loading the Dataset"""

# Download latest version
path = kagglehub.dataset_download("nathaniellybrand/los-angeles-crime-dataset-2020-present")

print("Path to dataset files:", path)

#List the files in the downloaded dataset directory
files = os.listdir(path)
print("Files in the downloaded dataset directory:", files)

# Load the dataset
file_name = 'Crime_Data_from_2020_to_Present.csv'  # Adjust as necessary
file_path = os.path.join(path, file_name)

# Read the CSV file
crime_df = pd.read_csv(file_path)

"""## Exploratory Data Analysis"""

crime_df.head()

crime_df.info()

crime_df.describe()

CrmCdDesc_counts = crime_df['Crm Cd Desc'].value_counts()

print(CrmCdDesc_counts)

CrmCdDesc_counts_list = CrmCdDesc_counts.tolist()

print(CrmCdDesc_counts_list)

# Get the list of unique values in 'Crm Cd Desc' ordered by their count
CrmCdDesc_list = CrmCdDesc_counts.index.tolist()

# Display the result
print(CrmCdDesc_list)

# Pie chart for the Summary column
def pie_chart_CrmCdDesc():

  # autopct defines the wedges or the numeric values shown in the pie chart
  plt.pie(CrmCdDesc_counts_list, labels = CrmCdDesc_list, autopct = '%1.1f%%')
  plt.title('Pie Chart of Crm Cd Desc')
  plt.show()

pie_chart_CrmCdDesc()

"""As we can see from the pie chart above, the most committed crime in the dataset is **VEHICLE - STOLEN** with **10.7%**. Next are **BATTERY - SIMPLE ASSAULT** with **7.9%**, **THEFT OF IDENTITY** with **6.5%**, **BURGLARY FROM VEHICLE** with **6.2%**, and so on. As for the other crime types that are few in numbers, we will have to remove rows with these types in order to prevent biases in training the model due to the unbalanced dataset. This also means we will have to remove some rows with crime types that have high counts in the dataset."""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (adjust file path if necessary)
# crime_df = pd.read_csv('path_to_your_csv_file.csv')

# Count of crimes per area
crime_per_area = crime_df['AREA NAME'].value_counts()

# Plotting
plt.figure(figsize=(12, 8))
sns.barplot(x=crime_per_area.index, y=crime_per_area.values, palette='viridis')
plt.title('Crimes Committed per Area')
plt.xlabel('Area')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=45, ha='right')
plt.show()

"""As we can see from the bar graph above, the areas with the highest number of crimes are concentrated in specific regions. For instance, Central and Southwest areas report the most incidents, indicating these could be high-crime zones requiring more focused intervention. In contrast, some areas show lower crime counts, which may suggest varying levels of crime activity across regions. For accurate model training, we need to account for these differences to prevent our model from being biased toward high-crime areas and ensure fair representation of all areas in our predictions.

"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Filter out rows where Vict Age is 0 or less (no direct victim)
age_filtered_df = crime_df[crime_df['Vict Age'] > 0]

# Define age bins and labels for age groups
age_bins = [0, 17, 30, 45, 60, 120]
age_labels = ['Under 18', '18-30', '31-45', '46-60', 'Above 60']
age_filtered_df['Age Group'] = pd.cut(age_filtered_df['Vict Age'], bins=age_bins, labels=age_labels, right=False)

# Count of crimes by age group
crime_by_age_group = age_filtered_df['Age Group'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x=crime_by_age_group.index, y=crime_by_age_group.values, palette='magma')
plt.title('Crimes Committed by Victim Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Crimes')
plt.show()

"""The bar graph above reveals that certain age groups experience higher crime rates. The 18-30 and 31-45 age groups report the most incidents, suggesting that young adults and middle-aged individuals are more frequently targeted or involved in crime. In contrast, the Under 18 and Above 60 age groups show relatively lower crime counts, indicating a potential age-related trend in crime exposure. Recognizing these patterns is crucial, as it helps in understanding demographic vulnerabilities and can inform strategies for targeted interventions to protect these age groups.

## Data Cleaning
"""

crime_df.info()

# Checking for missing values
crime_df.isnull().sum()

"""We can see from the table that there are significantly many null values across many columns. These columns are **Mocodes**, **Weapon Used Cd**, **Weapon Desc**, **Crm Cd 2**, **Crm Cd 3**, **Crm Cd 4**, and **Cross Street**. We will have to drop them in a new data frame as well as the deemed unnecessary columns in predicting the types of crime committed such as **DR_NO**, **Date Rptd**, **Rpt Dist No**, **Status**, **Status Desc**, **Crm Cd 1**, **LOCATION**, **LAT**, and **LON**.

**Vict Sex**, **Vict Descent**, **Premis Cd**, and **Premis Desc** are necessary. And so, we will try to reduce the number of their null values.
"""

crime_df['Vict Age'].value_counts()

"""Ages **-1** and **-2** do not make sense and therefore should be interpreted the same as **0**."""

crime_df['Vict Sex'].value_counts()

crime_df['Vict Descent'].value_counts()

"""We will have to replace the null values in **Vict Sex** and **Vict Descent** with **'-'** because **'-'** values exist in these columns and are deemed to represent crimes where there are no victims directly involved."""

crime_df[['Premis Cd', 'Premis Desc']].value_counts()

"""On the other hand, **Premis Cd** and its corresponding column **Premis Desc** have null values that do not represent anything and are in few numbers. And so, we will have to drop the rows containing null values in said columns. We will also have to drop the row containing **803.0** and **805.0** in **Premis Cd** since its literal description is **RETIRED (DUPLICATE) DO NOT USE THIS CODE**."""

# Drop columns with excessive missing values
cols_to_drop = ['Mocodes', 'Weapon Used Cd', 'Weapon Desc', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street']
crime_df_cleaned = crime_df.drop(columns = cols_to_drop)

# Drop unnecessary columns
cols_to_drop = ['DR_NO', 'Date Rptd', 'Rpt Dist No', 'Status', 'Status Desc', 'Crm Cd 1', 'LOCATION', 'LAT', 'LON']
crime_df_cleaned = crime_df_cleaned.drop(columns = cols_to_drop)

# Replace -1 and -2 values in the 'Vict Age' column with 0
crime_df_cleaned['Vict Age'] = crime_df_cleaned['Vict Age'].replace([-1, -2], 0)

# Impute missing values in 'Vict Sex' and 'Vict Descent'
crime_df_cleaned.fillna({'Vict Sex': '-'}, inplace = True)
crime_df_cleaned.fillna({'Vict Descent': '-'}, inplace = True)

# Drop rows with missing values in 'Premis Cd' and 'Premis Desc'
crime_df_cleaned.dropna(subset = ['Premis Cd'], inplace = True)
crime_df_cleaned.dropna(subset = ['Premis Desc'], inplace = True)

# Drop rows with 803.0 and 805.0 in 'Premis Cd'
crime_df_cleaned.drop(crime_df_cleaned[crime_df_cleaned['Premis Cd'].isin([803.0, 805.0])].index, inplace = True)

crime_df_cleaned.head()

# Recheck missing values
crime_df_cleaned.isnull().sum()

CrmCdDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()

CrmCdDesc_counts_list = CrmCdDesc_counts.tolist()
CrmCdDesc_list = CrmCdDesc_counts.index.tolist()

pie_chart_CrmCdDesc()

"""## Data Balancing"""

# Make 'Crm Cd Desc' the target variable
CrmDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()

# Filter out classes with a small number of occurrences
threshold_percentage = 4     # Adjust as desired
total_count = len(crime_df_cleaned)
threshold_count = total_count * (threshold_percentage / 100)

significant_classes = CrmDesc_counts[CrmDesc_counts >= threshold_count].index.tolist()

print(f"Original DataFrame size: {len(crime_df_cleaned)}")

# Filter the DataFrame to include only rows with significant classes
crime_df_cleaned = crime_df_cleaned[crime_df_cleaned['Crm Cd Desc'].isin(significant_classes)]

print(f"Filtered DataFrame size: {len(crime_df_cleaned)}")

# Now 'crime_df_cleaned' contains only rows with the most significant crime types.
# We can proceed with further cleaning, preprocessing, and model training using 'crime_df_cleaned'.

crime_df_cleaned.head()

if 'Crm Cd Desc' in crime_df_cleaned.columns:
    CrmDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()
    print("Class Distribution:\n", CrmDesc_counts)

CrmCdDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()

CrmCdDesc_counts_list = CrmCdDesc_counts.tolist()
CrmCdDesc_list = CrmCdDesc_counts.index.tolist()

pie_chart_CrmCdDesc()

# Determine the minimum number of samples in any class.
min_samples = CrmDesc_counts.min()

# Create an empty list to store the balanced samples.
balanced_df_list = []

# Iterate through each class and resample to match the minimum number of samples.
for crime_type in CrmDesc_counts.index:
  class_df = crime_df_cleaned[crime_df_cleaned['Crm Cd Desc'] == crime_type]
  resampled_df = resample(
      class_df,
      replace=True,  # Sample with replacement to ensure the same number of samples for each class.
      n_samples=min_samples,
      random_state=42,  # Set a random seed for reproducibility.
  )
  balanced_df_list.append(resampled_df)

# Concatenate the resampled dataframes to replace crime_df_cleaned with it.
crime_df_cleaned = pd.concat(balanced_df_list)

# Shuffle the balanced dataset.
crime_df_cleaned = crime_df_cleaned.sample(frac=1, random_state=42)

# Check the class distribution after balancing.
CrmDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()
print("Balanced Class Distribution:\n", CrmDesc_counts)

# Now 'crime_df_cleaned' contains a balanced dataset with equal representation of each class.
# We can proceed using the new 'crime_df_cleaned'.

CrmCdDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()

CrmCdDesc_counts_list = CrmCdDesc_counts.tolist()
CrmCdDesc_list = CrmCdDesc_counts.index.tolist()

pie_chart_CrmCdDesc()

"""## Data Preprocessing"""

crime_df_cleaned.info()

"""Values in **Premis Cd** are in float datatype even though there are no decimal numbers in these values. We will convert them to int datatype to maintain consistency."""

# Convert 'Premis Cd' to int
crime_df_cleaned['Premis Cd'] = crime_df_cleaned['Premis Cd'].astype(int)
print("Data type of 'Premis Cd' after conversion:", crime_df_cleaned['Premis Cd'].dtype)

"""Values in **DATE OCC** are in object datatype. We need to convert them to datetime format."""

# Convert 'DATE OCC' to datetime format
# errors="coerce" prevents the halting of the code execution even if there are any raised errors.
crime_df_cleaned['DATE OCC'] = pd.to_datetime(crime_df_cleaned['DATE OCC'], errors='coerce')

crime_df_cleaned['DATE OCC'].head()

# Check the data type after conversion
print("Data type of 'DATE OCC' after conversion:", crime_df_cleaned['DATE OCC'].dtype)

"""We will convert **TIME OCC** values into strings to extract the hour values later on. Minutes are deemed to be too extra."""

# Convert 'TIME OCC' to string
crime_df_cleaned['TIME OCC'] = crime_df_cleaned['TIME OCC'].astype(str).str.zfill(4)
print("Data type of 'TIME OCC' after conversion:", crime_df_cleaned['TIME OCC'].dtype)

# Check for NaT values in 'DATE OCC' and 'TIME OCC'
nat_rows_date = crime_df_cleaned[crime_df_cleaned['DATE OCC'].isna()]
nat_rows_time = crime_df_cleaned[crime_df_cleaned['TIME OCC'].isna()]

# Display the rows with NaT values
print("Rows with NaT in 'DATE OCC': ")
print(nat_rows_date)
print("Rows with NaT in 'TIME OCC': ")
print(nat_rows_time)

# Optionally, print the number of NaT values
print(f"Number of NaT values in 'DATE OCC': {nat_rows_date.shape[0]}")
print(f"Number of NaT values in 'TIME OCC': {nat_rows_time.shape[0]}")

"""We will then create new features from the date. **Month**, and **Hour** are included while **Year**, **Day** and **Minute** are excluded."""

# Create new features from the date
crime_df_cleaned['Month'] = crime_df_cleaned['DATE OCC'].dt.month
crime_df_cleaned['Hour'] = crime_df_cleaned['TIME OCC'].str[:2].astype(int)

crime_df_cleaned.head()

"""Since **Crm Cd Desc** already has their own encoded values in **Crm Cd**, we will map them."""

# Mapping of the Crm Cd Desc and their encoded equivalent

unique_CrmCdDesc = crime_df_cleaned['Crm Cd Desc'].unique()
unique_CrmCd = crime_df_cleaned['Crm Cd'].unique()

# Create a new DataFrame
CrmCdDesc_mapping_df = pd.DataFrame({'Crm Cd Desc': unique_CrmCdDesc, 'Crm Cd': unique_CrmCd})

# Display the DataFrame
CrmCdDesc_mapping_df

"""**AREA NAME** also has their own encoded values **AREA**. We will map them."""

# Mapping of the AREA NAME and their encoded equivalent

unique_AreaName = crime_df_cleaned['AREA NAME'].unique()
unique_Area = crime_df_cleaned['AREA'].unique()

# Create a new DataFrame
AreaName_mapping_df = pd.DataFrame({'AREA NAME': unique_AreaName, 'AREA': unique_Area})

# Display the DataFrame
AreaName_mapping_df

"""The same goes for **Premis Desc** and **Premis Cd**. We will map them."""

# Mapping of the Premis Desc and their encoded equivalent

unique_PremisDesc = crime_df_cleaned['Premis Desc'].unique()
unique_PremisCd = crime_df_cleaned['Premis Cd'].unique()

# Create a new DataFrame
PremisDesc_mapping_df = pd.DataFrame({'Premis Desc': unique_PremisDesc, 'Premis Cd': unique_PremisCd})

# Display the DataFrame
PremisDesc_mapping_df

encoder = LabelEncoder()

"""Since **Vict Sex** does not have their own encoded values, we will encode them."""

crime_df_cleaned['Vict Sex Encoded'] = encoder.fit_transform(crime_df_cleaned['Vict Sex'])

crime_df_cleaned.head()

"""We will create a mapping for them as well."""

# Mapping of the Vict Sex and their encoded equivalent

unique_VictSex = crime_df_cleaned['Vict Sex'].unique()
unique_VictSexEncoded = crime_df_cleaned['Vict Sex Encoded'].unique()

# Create a new DataFrame
VictSex_mapping_df = pd.DataFrame({'Vict Sex': unique_VictSex, 'Vict Sex Encoded': unique_VictSexEncoded})

# Display the DataFrame
VictSex_mapping_df

"""The same goes for **Vict Descent**."""

crime_df_cleaned['Vict Descent Encoded'] = encoder.fit_transform(crime_df_cleaned['Vict Descent'])

crime_df_cleaned.head()

# Mapping of the Vict Descent and their encoded equivalent

unique_VictDescent = crime_df_cleaned['Vict Descent'].unique()
unique_VictDescentEncoded = crime_df_cleaned['Vict Descent Encoded'].unique()

# Create a new DataFrame
VictDescent_mapping_df = pd.DataFrame({'Vict Descent': unique_VictDescent, 'Vict Descent Encoded': unique_VictDescentEncoded})

# Display the DataFrame
VictDescent_mapping_df

CrmCdDesc_counts = crime_df_cleaned['Crm Cd Desc'].value_counts()

CrmCdDesc_counts_list = CrmCdDesc_counts.tolist()
CrmCdDesc_list = CrmCdDesc_counts.index.tolist()

pie_chart_CrmCdDesc()

"""## Model Training"""

# Select features and target variable
features = ['AREA', 'Part 1-2', 'Vict Age', 'Premis Cd', 'Month',
            'Hour', 'Vict Sex Encoded', 'Vict Descent Encoded']
X = crime_df_cleaned[features]
y = crime_df_cleaned['Crm Cd']

X.head()

y.head()

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

X_train.shape

X_train.head()

X_test.shape

X_test.head()

y_train.shape

y_train.head()

y_test.shape

y_train.head()

# Train the Random Forest Classifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Feature Importance
random_forest_feature_importance = pd.Series(model.feature_importances_, index=X_train.columns)

random_forest_feature_importance

# Plot feature importances
plt.figure(figsize=(10, 6))
sns.barplot(x=random_forest_feature_importance, y=random_forest_feature_importance.index)
plt.title("Random Forest Classifier Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()

"""## Predictions"""

# Manual Data

# Creating a new manual set of data using existing data as tests
df_head = crime_df_cleaned.head().copy()
df_tail = crime_df_cleaned.tail().copy()

# Concatenate head and tail into a new DataFrame
df_new = pd.concat([df_head, df_tail], ignore_index=True)

df_new

# Drop the 'Crm Cd Desc' column
df_new_dropped = df_new.drop(columns=['Crm Cd Desc'])

df_new_dropped

model

# Show the mapping
CrmCdDesc_mapping_df

def predict_crime_type(df_new):
  # Ensure the new DataFrame is a copy to prevent changes to the original
    df_new = df_new.copy()

    # Encode the new data with mappings
    df_new['AREA'] = df_new['AREA NAME'].map(AreaName_mapping_df.set_index('AREA NAME')['AREA'])
    df_new['Vict Sex Encoded'] = df_new['Vict Sex'].map(VictSex_mapping_df.set_index('Vict Sex')['Vict Sex Encoded'])
    df_new['Vict Descent Encoded'] = df_new['Vict Descent'].map(VictDescent_mapping_df.set_index('Vict Descent')['Vict Descent Encoded'])
    df_new['Premis Cd'] = df_new['Premis Desc'].map(PremisDesc_mapping_df.set_index('Premis Desc')['Premis Cd'])

    # Select only the required features for prediction
    X_new = df_new[['AREA', 'Part 1-2', 'Vict Age', 'Premis Cd', 'Month', 'Hour', 'Vict Sex Encoded', 'Vict Descent Encoded']]

    # Use the model to predict the class of the new data
    model_predictions_encoded = model.predict(X_new)

    # Map predictions to their corresponding descriptions
    df_new['Predicted Crm Cd'] = model_predictions_encoded
    df_new['Predicted Crm Cd Decoded'] = df_new['Predicted Crm Cd'].map(CrmCdDesc_mapping_df.set_index('Crm Cd')['Crm Cd Desc'])

    # Return the DataFrame with predictions
    return df_new[['Predicted Crm Cd', 'Predicted Crm Cd Decoded']]

df_new_predictions = predict_crime_type(df_new_dropped)

df_new

df_new_predictions

"""As it can be seen, the model correctly predicted the crime type for all rows in the manual test datasets, which is the head and tail of our cleaned dataframe, respectively.

## Conclusion

In this analysis, we focused on predicting crime types using a Random Forest Classifier model. We began with an unbalanced dataset containing **752,911** records and removed rows representing crime types that made up less than **4%** each of the total data. After this data cleaning and balancing process, the dataset was reduced to **341,505** rows, concentrating on the top nine crime types. This selection made us worked with the most frequently recorded crime types, including "`INTIMATE PARTNER - SIMPLE ASSAULT`", "`VEHICLE - STOLEN`", "`THEFT PLAIN - PETTY ($950 & UNDER)`", "`BURGLARY`", "`THEFT OF IDENTITY`", "`ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT`", "`BURGLARY FROM VEHICLE`", "`VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)`", and "`BATTERY - SIMPLE ASSAULT`"


1.   Model Training and Performance:

- We trained our `Random Forest Classifier` on selected features such as `AREA NAME`, `Part 1-2`, `Vict Age`, `Premis Desc`, `Month`, `Hour`, `Vict Sex`, and `Vict Descent`  to predict the crime category. After splitting the data, the model achieved an accuracy of **80.75%** on the test set. This performance indicates that our selected features provided substantial predictive power, though additional cleaning and balancing of data could potentially improve accuracy. But also means sacrificing another type of crime in the model training just so the accuracy would improve, and so we chose not to.

2.   Feature Importance Analysis:

- Analysis of feature importance within the `Random Forest Classifier` model highlighted key predictors: `Premis Cd` (location type) and `Vict Age` were the most influential features, contributing around 19% and 18.7% respectively to the model's predictions. Other important factors included `Part 1-2` (crime part category) and `AREA NAME`. The prominence of these features show the value of contextual and demographic data in crime prediction. Unexpectedly, `Vict Sex` had the lowest importance among all the features. Other less important features were not invaluable enough to be considered removed from the model training.


# Summary

Overall, this project demonstrated the viability of using a machine learning approach to predict crime types with a reasonable degree of **80.75%** accuracy. By focusing on a balanced subset of common crime types and the use of a Random Forest Classifier model, we were able to successfully find patterns in the data that correlate with different crime categories. Though many crime types have been excluded, this project could definitely be improved with the help of other model training tools.
"""