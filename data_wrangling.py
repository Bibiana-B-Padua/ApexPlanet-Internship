import pandas as pd

# 1. Load the Dataset
# Assuming the file is in the same directory as your script
file_path = 'ApexPlanet_DataAnalytics_Dataset.xlsx'
df = pd.read_excel(file_path, sheet_name='Sales_Dataset')

print("--- Initial Data Profiling ---")
print(df.info())
print("\nMissing Values Count:\n", df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

# 2. Data Cleaning & Transformation
# Handle Duplicates
df = df.drop_duplicates()

# Standardize Date Format (Ensuring it's a datetime object)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Ensure categorical fields are standardized (e.g., title case to avoid 'male' vs 'Male')
df['Gender'] = df['Gender'].str.title()
df['City'] = df['City'].str.title()
df['Category'] = df['Category'].str.title()

# Feature Engineering: Create an 'Age Group' column from the 'Age' column
# This is similar to the task's suggestion of creating 'Age' from 'DOB'
bins = [0, 18, 30, 45, 60, 100]
labels = ['<18', '19-30', '31-45', '46-60', '60+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# Validation Check: Ensure Total_Sales actually equals Quantity * Unit_Price
# (Floating point arithmetic can sometimes cause tiny discrepancies, so we round)
df['Calculated_Total'] = (df['Quantity'] * df['Unit_Price']).round(2)
df['Total_Sales'] = df['Total_Sales'].round(2)

inconsistencies = df[df['Calculated_Total'] != df['Total_Sales']]
if not inconsistencies.empty:
    print(f"\nWarning: Found {len(inconsistencies)} rows where Total_Sales does not match Quantity * Unit_Price.")
    # Optional: Force the correct calculation
    # df['Total_Sales'] = df['Calculated_Total']

# Drop the temporary calculation column
df = df.drop(columns=['Calculated_Total'])

# 3. Output the Final Dataset
output_path = 'Cleaned_Sales_Dataset.csv'
df.to_csv(output_path, index=False)
print(f"\nCleaning complete. Analysis-ready dataset saved to '{output_path}'.")
