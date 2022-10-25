#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:59:23 2022

@author: disha.dubey
"""

import pandas as pd
import numpy as np
import streamlit as st
import helper
import plotly.graph_objects as go
import plotly.express as px


#read data
telco_data = helper.load_data('master_dataset.csv')

st.set_page_config(
    page_title="Customer Churn Analysis",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header('Churn Analysis')
st.sidebar.header("Churn Analysis ")

#----------------1.create data for waterfall chart
total_cust_start = telco_data[telco_data['Customer_Status'] != 'Joined']['Customer_ID'].count()
total_cust_end = telco_data[telco_data['Customer_Status'] != 'Churned']['Customer_ID'].count()
x_list = telco_data[telco_data['Customer_Status']!= 'Stayed']['Customer_Status'].value_counts().index.tolist()
x_list.insert(0,'Total-start')
x_list.append('Total-end')
y_list = telco_data[telco_data['Customer_Status']!= 'Stayed']['Customer_Status'].value_counts().values.tolist()
y_list.insert(0,total_cust_start)
y_list.append(total_cust_end)
for i in range(len(x_list)):
    if x_list[i]== 'Churned':
        y_list[i]*=-1
    else:
        y_list[i]*=1
#---------------2. Calculate metrics to display
total_cust = y_list[0]
total_cust_delta = np.round((y_list[-1]-y_list[0])/y_list[0]*100)
new_cust = telco_data[telco_data['Customer_Status'] == 'Joined']['Customer_ID'].count()
new_cust_delta = 0.1
churn_rate = np.round((telco_data[telco_data['Customer_Status']=='Churned']['Customer_ID'].count()/total_cust_start)*100,2)
churn_rate_delta = 0.5

#-------------3. Prepare data for churned customers profile
#@st.cache
telco_data_churned = telco_data[telco_data['Churn_Label'] == 'Yes']
telco_data_churned.rename(columns = {'Latitude': 'latitude', 'Longitude':'longitude'}, inplace = True)
telco_data_churned_nrows = telco_data_churned.shape[0]

avg_age = round(telco_data_churned['Age'].mean())
per_under_30 = round(telco_data_churned[telco_data_churned['Under_30'] == 'Yes']['Customer_ID'].count()/telco_data_churned_nrows*100)
per_senior_citizen = round(telco_data_churned[telco_data_churned['Senior_Citizen'] == 'Yes']['Customer_ID'].count()/telco_data_churned_nrows*100)
per_female = round(telco_data_churned[telco_data_churned['Gender']== 'Female']['Customer_ID'].count()/telco_data_churned_nrows*100)
per_married = round(telco_data_churned[telco_data_churned['Married']== 'Yes']['Customer_ID'].count()/telco_data_churned_nrows*100)
metric_dict = {'Metric' : ['Age (avg)', 'Under 30yr (%)', 'Senior citizens (%)', 'Female (%)', 'Married (%)'],
'Value' :  [avg_age,per_under_30,per_senior_citizen,per_female,per_married]}
churn_profile = pd.DataFrame(data =metric_dict,columns = ['Metric', 'Value'])


churned_cust_by_zip = pd.DataFrame(telco_data_churned['Zip_Code'].value_counts().reset_index())
churned_cust_by_zip.columns = ['Zipcode', '#Churned customers']
#=======

#---------Plotly's waterfall chart object declaration

fig = go.Figure(go.Waterfall(
    name = "#Customers", orientation = "v",
    measure = ['absolute','relative','relative','total'] ,
    #x = ['Total-start', 'Churn','joined','end'],
    x= x_list,
    textposition = "outside",
    #text = ["+60", "+80", "", "-40", "-20", "Total"],
    #y = [1000,-200,100,900],
    y= y_list,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))
fig.update_layout(
        #title = "Customer status",
        showlegend = False,
        width=1500,
        height=700
)
#Set y-limit
fig.update_yaxes(title = "#Customers")

#---A. Current state of customers/ churn rate story

col11 , col12, col13 = st.columns(3)
with col11:
    st.metric(label = 'Total customers(#)',value = total_cust, delta = total_cust_delta )
    
     #st.markdown()
    
with col12:
    st.metric(label = 'New customers(#)',value = new_cust, delta =new_cust_delta )

with col13:
    st.metric(label = 'Churn rate(%)',value = churn_rate, delta =churn_rate_delta, delta_color="inverse")

#Waterfall chart
st.caption('vs. last month',unsafe_allow_html=True)
#st.markdown('## Customer by status')
st.plotly_chart(fig,use_container_width=True,sharing="streamlit")

st.markdown('#### Churn Reason')
tab661, tab662 = st.tabs(["Bar","Pie"])
with tab661:
    fig2 = px.histogram(telco_data_churned, x="Churn_Category")
    st.plotly_chart(fig2,use_container_width=True,sharing="streamlit")
with tab662:
    fig3 = px.pie(telco_data_churned, names='Churn_Category')
    st.plotly_chart(fig3,use_container_width=True,sharing="streamlit")

#--------------B.How do these customers look like- demographics
st.markdown('#### Demographics profile')
col21, col22 = st.columns(2)

#placeholder for demographics profiling 
with col21:
    expander = st.expander("See explanation")
    expander.write("""
    Table below is a demographics profile of churned customers. Map on the right shows concentration of churned customers""")
    st.table(churn_profile)

#placeholder for map to show concentration
with col22:
    tab221, tab222 = st.tabs(["📈 Chart", "🗃 Data"])
    with tab221:
        st.map(telco_data_churned[['latitude', 'longitude']])
    with tab222:
        st.dataframe(churned_cust_by_zip)
        st.map(telco_data_churned[['latitude', 'longitude']])

#-------------C. Relationship and usage stats