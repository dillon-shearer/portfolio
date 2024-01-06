#!/usr/bin/env python
# coding: utf-8

# ##### Import Libraries 

# In[6]:


import pandas as pd
import requests
from io import BytesIO

# ##### Filepath to Census SAIPE 2022 National/State/County Poverty Data

# In[7]:


download_filepath = f'https://www2.census.gov/programs-surveys/saipe/datasets/2022/2022-state-and-county/est22all.xls'

# ##### Load data from filepath

# In[8]:


# Download the Excel file from the URL
response = requests.get(download_filepath)
excel_data = response.content

# Read the downloaded Excel file using pandas
df = pd.read_excel(BytesIO(excel_data))

# ##### Check dataframe

# In[9]:


df.head()

# ##### Save to **census_Poverty/data/RAW_2022_SAIPE_DATA.xlsx**

# In[10]:


out_filepath = f'../census_Poverty/data/RAW_2022_SAIPE_DATA.xlsx'
df.to_excel(out_filepath, index=False)
