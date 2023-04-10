import streamlit as st
import eda
import ChurnModel

# Create navigation function
navigation = st.sidebar.selectbox('Pilih Halaman : ', ('EDA', 'Data Prediction'))

if navigation == 'EDA':
    eda.run()
else:
    ChurnModel.run()