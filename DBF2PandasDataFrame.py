# coding: utf-8 # In[1]:
import pandas as pd
from simpledbf import Dbf5

# In[2]:
dbf = Dbf5('gem_2016.dbf')

# In[3]:
df = dbf.to_dataframe()

# In[4]:
df.head() 
