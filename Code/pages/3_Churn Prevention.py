#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on 10/23/22
#author: Kevin Soderholm


import pandas as pd
import numpy as np
import streamlit as st
import helper
import plotly.graph_objects as go


#read data
telco_data = helper.load_data('master_dataset_scored.csv')

st.set_page_config(
    page_title="Customer Churn Analysis",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",)
st.header('Churn Prevention')
st.sidebar.header("Churn Prevention")

#prep data
pd.set_option('mode.chained_assignment', None)
telco_data_predchurned = telco_data[telco_data['ypredfull'] == 1]
telco_data_predchurned.rename(columns = {'Latitude': 'latitude', 'Longitude':'longitude', 'ypredptfull':'PredProb'}, inplace=True)
telco_data_predchurned_nrows = telco_data_predchurned.shape[0]
telco_data_predchurned_contract=telco_data_predchurned[telco_data_predchurned['contract_flag'] == 0]
telco_data_predchurned_bundle=telco_data_predchurned[telco_data_predchurned['contract_flag'] > 0]

#create submission form within container
with st.container():
    with st.form("prediction_form"):
        st.markdown("**Campaigns:**")
        st.markdown("**Annual Contract Offer** - _this is for predicted churns that are currently on a month to month contract.  Reach out to customers with a tiered discount offer to move to 1 or 2 year contracts._")
        st.markdown("**Product/Service Bundle Offer** - _this is for predicted churns with high monthly costs per household member.  Reach out to customers with a discount offer to bundle products and services to retain these high value customers._")
        Campaign_Type = st.radio("Select Campaign:",('Annual Contract Offer', 'Product/Service Bundle Offer'))
        submitted = st.form_submit_button("Get campaign data")
        if submitted:
            if Campaign_Type == 'Annual Contract Offer':
                tab51, tab52 = st.tabs(["Map", "Campaign List"])
                with tab51:
                    st.map(telco_data_predchurned_contract[['latitude', 'longitude']])
                with tab52:
                    st.dataframe(telco_data_predchurned_contract[['Customer_ID','Gender','Age','Contract','City','Zip_Code','Location_ID','PredProb']])
            else:
                tab61, tab62 = st.tabs(["Map", "Campaign List"])
                with tab61:
                    st.map(telco_data_predchurned_bundle[['latitude', 'longitude']])
                with tab62:
                    st.dataframe(telco_data_predchurned_bundle[['Customer_ID','Gender','Age','mc_hh_ratio','total_nbr_srvcs','City','Zip_Code','Location_ID','PredProb']])
                    
                    