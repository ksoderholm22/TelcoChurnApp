#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:59:23 2022

@author: Disha Dubey,kevin soderholm
"""

import pandas as pd
import numpy as np
import streamlit as st
import helper
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk

#read data
telco_data_scored = pd.read_csv('churn_prediction.csv')
master_data_scored = pd.read_csv('master_dataset_scored.csv')
pd.set_option('mode.chained_assignment', None)
master_data_scored.rename(columns = {'ypredfull':'PredClass','ypredptfull':'PredProb'}, inplace=True)

#------------ create dataframe for prediction importnace
fi_data = pd.DataFrame({'Feature': ['Monthly charges', 'Household size' ,'Internet plan type', 'charge to household size ratio', 'Customer age', 'Tenure to age ratio', '#Referrals', 'Contract type']
 ,'Importance':[0.005,0.006,0.007,0.013,0.014,0.039,0.047,0.074]
 ,'Normalized importance':[0.063,0.081,0.101,0.175,0.193,0.521,0.632,1]
 })

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header("Churn prediction")
st.sidebar.header("Churn Prediction ")

tab11, tab12 = st.tabs(["Get prediction", "View scores"])
with tab11:
    with st.form("prediction_form"):
        st.markdown("**Enter customer attributes to know their churn risk**")
        
        colf1, colf2 = st.columns(2)
        with colf1:
            internet_type_flag = st.number_input('Insert internet plan', value = 0, min_value=0,max_value=2)
            contract_flag = st.number_input('Insert contract type', value =2, min_value=0,max_value=2)
        
        with colf2:
            mc_hh_ratio = st.number_input('Insert monthly charge by household size',step=10, value =10, min_value=0, max_value=200)
            Number_of_Referrals = st.number_input('Insert referral count', step=3, value =9, min_value=0, max_value=15)
        submitted = st.form_submit_button("Get churn score")
        if submitted:
            try:
                churn_score = telco_data_scored.loc[(round(telco_data_scored['internet_type_flag'])== internet_type_flag) & (round(telco_data_scored['contract_flag'])== contract_flag) & (helper.myround(telco_data_scored['mc_hh_ratio'],10) == mc_hh_ratio) & (helper.myround(telco_data_scored['Number_of_Referrals'],3) == Number_of_Referrals ),'ypredptfull']
                churn_score2=churn_score.mean()
                churn_score3=churn_score2.round(4)
                st.write('With a churn score of: ', churn_score3)
                if churn_score3>0.5:
                    st.write('This customer is at **high** risk of churn')
                if 0.3<churn_score3<0.5:
                    st.write('This customer is at **medium** risk of churn')
                if churn_score3<0.3:
                    st.write('This customer is at **low** risk of churn')
            except:
                st.write('No customers in this segment')

with tab12:
    st.dataframe(master_data_scored[['Customer_ID','contract_flag','Number_of_Referrals','tenure_age_ratio','Age','mc_hh_ratio','internet_type_flag','hh_size','Monthly_Charge','City','Zip_Code','Location_ID','PredClass','PredProb']])
    
# Feature importance
tab21, tab22 = st.tabs(["📈 Chart", "🗃 Data"])
#st.subheader("Churn Prediction drivers")
with tab21:
    fig = px.bar(fi_data, x="Normalized importance", y="Feature", orientation='h',title = "Churn prediction drivers")
    st.plotly_chart(fig)
with tab22:
    st.dataframe(fi_data)

#Model Info

expander = st.expander("Model Information")
expander.write("""**Model Name:** Churn Model 1.0""")
expander.write("""**Model ID:** 123456""")
expander.write("""**Model Purpose:** Predict likelihood of customer churn within 3 months""")
expander.write("""**Model Algorithm:** XGBoost Classifier (n_estimators=100, max_depth=3, learning rate=0.05)""")
expander.write("""**Model Owners:** Brendan Miller, Disha Dubey, Kevin Soderholm""")
expander.write("""**Production Date:** 10/25/2022""")











