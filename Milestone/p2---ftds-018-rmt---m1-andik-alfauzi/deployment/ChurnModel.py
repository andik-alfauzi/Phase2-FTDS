import numpy as np
import pandas as pd
import streamlit as st
import pickle
from datetime import datetime
from tensorflow.keras.models import load_model

# load the model 
baseFunctional = load_model('churnModel.h5')

with open('FinalPipeline.pkl', 'rb') as file1:
   finalPipeline = pickle.load(file1)

def run():
    
    def age_bin(age):
      if age > 7 and age < 20:
        return 'under20'
      elif age >= 20 and age < 30:
        return 'under30'
      elif age >= 30 and age < 40:
         return 'under40'
      elif age >= 40 and age < 50:
         return 'under50'
      elif age >= 50 and age < 60:
         return 'under60'
      else:
        return 'above60'
    
  # membuat input data baru
    with st.form(key='churn_form'):
      age = st.number_input('Age', min_value=5, max_value=120, value=10, step=1, help='Usia Customer')
      gender = st.selectbox('Gender', ('Female', 'Male'))
      region_category = st.selectbox('Region Category', ('Village', 'Town', 'City'))
      membership_category = st.selectbox('Membership Category', ('No Membership', 'Basic Membership', 'Silver Membership',
                                                                 'Premium Membership', 'Gold Membership', 'Platinum Membership'))
      joining_date = st.date_input('Joining Date')
      medium_of_operation = st.selectbox('Medium of Operation', ('Smartphone', 'Desktop', 'Both'))
      preferred_offer_types = st.selectbox('Preferred Offer Types', ('Without Offers', 'Credit/Debit Card Offers', 'Gift Vouchers/Coupons'))
      days_since_last_login	= st.number_input('Days Since Last Login', value=1, min_value=1, max_value=150, step=1)
      avg_time_spent = st.number_input('Average Time Spent', min_value=0.00, step=0.10, value=0.00, format='%.2g')
      avg_transaction_value = st.number_input('Average Transaction Value', min_value=0.00, step=0.10, value=0.00, format='%.2g')
      avg_frequency_login_days = st.number_input('Average Frequency Login Days', min_value=0, step=1, value=0, max_value=120)
      points_in_wallet = st.number_input('Points in Wallet', min_value=0.00, step=0.10, value=0.00, format='%.2g')
      used_special_discount = st.selectbox('Used Special Discount', ('No', 'Yes'))
      offer_application_preference = st.selectbox('Offer Application Preference', ('Yes', 'No'))
      past_complaint = st.selectbox('Past Complaint', ('No', 'Yes'))
      complaint_status = st.selectbox('Complaint Status', ('No Information Available', 'Not Applicable', 'Unsolved', 'Solved', 'Solved in Follow-up'))
      feedback = st.selectbox('Feedback', ('Reasonable Price', 'Poor Website', 'Poor Customer Service', 'Too many ads', 'Poor Product Quality', 'No reason specified',
                                           'Products always in Stock', 'Quality Customer Care', 'User Friendly Website'))
      st.markdown('---')
      
      binAge = age_bin(age)
      
      submitted = st.form_submit_button('Predict')

      if joining_date:
        year = joining_date.year
        ('Tahun', year)
        
    infData = {
       'region_category' : region_category,
       'membership_category' : membership_category,
       'medium_of_operation' : medium_of_operation,
       'preferred_offer_types' : preferred_offer_types,
       'days_since_last_login' : days_since_last_login,
       'avg_time_spent' : avg_time_spent,
       'avg_transaction_value' : avg_transaction_value,
       'avg_frequency_login_days' : avg_frequency_login_days,
       'points_in_wallet' : points_in_wallet,
       'used_special_discount' : used_special_discount,
       'offer_application_preference' : offer_application_preference,
       'past_complaint' : past_complaint,
       'complaint_status' : complaint_status,
       'feedback' : feedback,
       'age_bin' : binAge,
       'joining_year' : year
    }

    infData = pd.DataFrame([infData])
    st.dataframe(infData)

    infPipe = finalPipeline.transform(infData)

    # Buat function di column submitted
    if submitted:
        
        # Predict using Base Functional API
        y_predInfData = baseFunctional.predict(infPipe)
        if y_predInfData >= 0.5:
           st.write('## Customer is Churn : Yes')
        else :
           st.write('## Customer is Churn : No')

if __name__ == '__main__':
   run()