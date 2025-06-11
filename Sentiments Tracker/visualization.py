#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
from pymongo import MongoClient


# In[3]:


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://USER:PASSWORD@cluster0.hxf1k2u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["AI_NEWS"]
collection = db["NewsAnalysis"]


# In[17]:


data = list(collection.find())


# In[18]:


sentiments = []
for entry in data:
    for item in entry['sentiments']:
        item_with_date = item.copy()
        item_with_date['date'] = entry['date'].date()
        sentiments.append(item_with_date)

df = pd.DataFrame(sentiments)


# # Streamlit

# In[ ]:


st.title("Sentiment Trend by Organization")

organization = st.selectbox("Select an organization", ['Microsoft','Apple'])

selected_df = df.loc[df['organization'] == organization].set_index('date')

st.line_chart(selected_df[['positive','negative','neutral']])

