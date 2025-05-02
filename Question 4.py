import pandas as pd

# Load data
df = pd.read_csv("Employee_census_data.csv")

##### Question 4a #####

# Step 1: Count how many times each eeid appears as a supervisor (supid) → this is soc
soc = df['supid'].value_counts().rename_axis('eeid').reset_index(name='soc')

# Step 2: Merge soc back into the original data
df = df.merge(soc, on='eeid', how='left')

# Fill soc=0 for employees who don't supervise anyone
df['soc'] = df['soc'].fillna(0).astype(int)

# Step 3: Create 'supervisor' dummy
df['supervisor'] = (df['soc'] > 0).astype(int)

# Check final dataframe
print(df.head())

# Step 4: Crosstab to validate soc vs supervisor
print(pd.crosstab(df['soc'], df['supervisor']))
