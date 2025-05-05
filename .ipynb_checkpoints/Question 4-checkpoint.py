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

##### Question 4b #####

def compute_soc_total(df):
    # Initialize soc_total with soc values
    df['soc_total'] = df['soc']

    # Convert to a dictionary for quick lookup
    soc_dict = df.set_index('eeid')['soc_total'].to_dict()
    sup_dict = df.groupby('supid')['eeid'].apply(list).to_dict()

    # Recursive function to compute soc_total for an employee
    def get_soc_total(eeid):
        total = soc_dict.get(eeid, 0)
        for subordinate in sup_dict.get(eeid, []):
            total += get_soc_total(subordinate)
        return total

    # Apply to all employees
    df['soc_total'] = df['eeid'].apply(get_soc_total)
    return df

# Apply the function
df = compute_soc_total(df)

# Check results
print(df[['eeid', 'soc', 'soc_total']])

### TESTS FOR IMPLICATIONS ###

# 1. CEO soc_total should be 104
ceo_soc_total = df.loc[df['eeid'] == 'p00578', 'soc_total'].iloc[0]
assert ceo_soc_total == 104, f"CEO soc_total expected to be 104 but got {ceo_soc_total}"
print("✅ Test 1 passed: CEO soc_total is 104")

# 2. Sum of soc_total for grade 6 employees should be 102
grade6_soc_total = df.loc[df['grade'] == 6, 'soc_total'].sum()
assert grade6_soc_total == 102, f"Grade 6 soc_total sum expected to be 102 but got {grade6_soc_total}"
print("✅ Test 2 passed: Grade 6 soc_total sums to 102")

# 3. For grade 2 employees, soc and soc_total should be equal
grade2 = df.loc[df['grade'] == 2]
mismatch = grade2[grade2['soc'] != grade2['soc_total']]
assert mismatch.empty, f"Grade 2 employees have soc != soc_total: {mismatch}"
print("✅ Test 3 passed: For all grade 2 employees, soc equals soc_total")

