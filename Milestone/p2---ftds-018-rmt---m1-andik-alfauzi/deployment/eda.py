import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title = 'Phase 2 - Milestone 1',
    layout = 'wide',
    initial_sidebar_state='expanded'
)

def run():
    # Buat title
    st.title('Churn Customer Prediction')

    # Buat sub header
    st.subheader('EDA untuk Analisa Dataset Churn')

    # Menambahkan gambar
    # Define function gambar
    image = Image.open('Dataset_Explain.png')
    # Function implementation
    st.image(image, caption='Dataset_Explain')

    # Menambahkan deskripsi
    st.write('Page made by *Andik Al Fauzi*')

    # Membuat garus lurus
    st.markdown('----')

    # Explaination of model deployment
    '''
    Pada Page kali ini, penulis akan melakukan explorasi sederhana.
    Dataset yang dipakai adalah dataset Churn yang diambil dari Assignment Milestone
    Project ini adalah instruksi dari Assignment di Milestone 1 Phase 2
    '''

    # Show dataframe
    data = pd.read_csv('https://raw.githubusercontent.com/andik-alfauzi/Phase2-FTDS/main/Milestone/p2---ftds-018-rmt---m1-andik-alfauzi/churn.csv')
    st.dataframe(data)

    # Membuat Histogram Age
    st.write('### Histogram of Age')
    fig = plt.figure(figsize=(15, 6))
    sns.histplot(data['age'], bins=50, kde=True)
    st.pyplot(fig)

    # Plotly age vs time spent
    fig = go.Figure(data=[go.Scatter3d(
        x = data['avg_time_spent'],
        y = data['avg_frequency_login_days'],
        z = data['age'],
        mode='markers',
        marker=dict(
            size = 10,
            color = data['age'],
            colorscale = 'Viridis',
            opacity = 0.8
        ),
        text = data['avg_time_spent'],
        hoverinfo='text'
    )])

    fig.update_layout(
        scene = dict(
            xaxis = dict(title='avg_time_spent'),
            yaxis = dict(title='avg_frequency_login_days'),
            zaxis = dict(title='age')
        ),
        title = 'User Infograpic by Age'
    )

    st.plotly_chart(fig)

    # Membuat Histogram base on user input
    st.write('#### Histogram base on user input')
    pilihan = st.selectbox('Pilih Column : ', ('avg_time_spent', 'avg_transaction_value', 'avg_frequency_login_days', 'points_in_wallet'))
    fig = plt.figure(figsize=(15, 5))
    sns.histplot(data[pilihan], bins=30, kde=True)
    st.pyplot(fig)

if __name__ == '__main__':
    run()