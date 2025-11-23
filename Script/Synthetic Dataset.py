import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
Faker.seed(42)

#Parameters
n_contracts = 200

#Categories
client_types = ['EU Institution', 'International Organization', 'Government Agency', 'Private Sector']
service_types = ['Software Development', 'Business Analysis', 'Project Management',
                 'Data Analysis', 'System Architecture', 'Quality Assurance']
statuses = ['Active', 'Completed', 'Expiring Soon', 'Renewed']
departments = ['IT Services', 'Finance Operations', 'HR Technology', 'Data Management', 'Procurement']
regions = ['Brussels', 'Vienna', 'Luxembourg', 'Remote', 'Athens']
levels = ['Junior', 'Mid-Level', 'Senior', 'Lead']
renewal_likelihood = ['High', 'Medium', 'Low']

#Generate data
data = []

for i in range(n_contracts):
    contract_id = f"CONT-{random.randint(2022, 2024)}-{str(i + 1).zfill(3)}"

    #Dates
    start_date = fake.date_between(start_date='-3y', end_date='today')
    duration_months = random.choice([6, 12, 18, 24, 36])
    end_date = start_date + timedelta(days=duration_months * 30)

    #Contract value based on level and duration
    level = random.choice(levels)
    base_rate = {'Junior': 50000, 'Mid-Level': 75000, 'Senior': 100000, 'Lead': 150000}
    contract_value = base_rate[level] * (duration_months / 12) * random.uniform(0.9, 1.1)

    #Status logic
    days_until_end = (end_date - datetime.now().date()).days
    if days_until_end < 0:
        status = random.choice(['Completed', 'Renewed'])
    elif days_until_end < 60:
        status = 'Expiring Soon'
    else:
        status = 'Active'

    #Renewal likelihood based on status and random factor
    if status == 'Renewed' or status == 'Completed':
        renewal = 'N/A'
    else:
        renewal = random.choice(renewal_likelihood)

    data.append({
        'Contract_ID': contract_id,
        'Client_Type': random.choice(client_types),
        'Service_Type': random.choice(service_types),
        'Contract_Value': round(contract_value, 2),
        'Start_Date': start_date,
        'End_Date': end_date,
        'Status': status,
        'Department': random.choice(departments),
        'Region': random.choice(regions),
        'Consultant_Level': level,
        'Renewal_Likelihood': renewal
    })

#Create DataFrame
df = pd.DataFrame(data)

#For date columns
df['Start_Date'] = pd.to_datetime(df['Start_Date']).dt.date
df['End_Date'] = pd.to_datetime(df['End_Date']).dt.date

#Calculate additional fields
df['Duration_Months'] = ((pd.to_datetime(df['End_Date']) - pd.to_datetime(df['Start_Date'])).dt.days / 30).round(0)
df['Days_Until_End'] = (pd.to_datetime(df['End_Date']) - pd.Timestamp(datetime.now().date())).dt.days
df['Value_Category'] = pd.cut(
    df['Contract_Value'],
    bins=[0, 50000, 100000, 200000, float('inf')],
    labels=['Small', 'Medium', 'Large', 'Strategic']
)

# Save to Excel
df.to_excel('contract_portfolio_data.xlsx', index=False, sheet_name='Contracts')

print(f"Generated {len(df)} contracts")
print(f"\nSummary Statistics:")
print(f"Total Portfolio Value: €{df['Contract_Value'].sum():,.2f}")
print(f"Average Contract Value: €{df['Contract_Value'].mean():,.2f}")
print(f"\nStatus Distribution:")
print(df['Status'].value_counts())
