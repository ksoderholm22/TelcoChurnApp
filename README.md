# TelcoChurnApp
This project is to showcase descriptive, predictive, and prescriptive analytics on synthetic Telco Churn dataset.

File descriptions

Prep/Analysis/Modeling:
data_prep.ipynb - importing, joining and prepping data for analysis
telco_model.ipynb - quick and dirty ML modeling workflow
modelpreds.ibynb - final model used for scoring dataset

Streamlit App:
helper.py - helper functions
requirements.txt - additional installations required by streamlit (anything not included in base python)
1_Churn_Analysis.py - "Churn Analysis" page
2_Churn_Prediction.py - "Churn Prediction" page
3_Churn_Prevention.py - "Churn Prevention" page

Data:
master_dataset.csv - original dataset used for modeling
master_dataset_scored.csv - original dataset + added engineered features and model predictions
churn_prediction.csv - used for widget on "Churn Prediction" page






