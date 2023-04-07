from os import access
from PIL import Image
from io import BytesIO
import requests
import numpy as np
import streamlit as st
import tensorflow as tf

st.set_page_config(layout="centered", page_title="Fire Detection Prediction",
                    menu_items={
                                "Get Help": "https://www.linkedin.com/in/andik-al-fauzi/",
                                "Report a bug": "https://github.com/andik-alfauzi",
                                "About": "### Fire Detection Prediction App - By Andik Al Fauzi"})

# Load Model
model = tf.keras.models.load_model('imp_model.h5')

# Variable for image
img = None

# Prediction
def img_predict(img):
    pred = np.array(img)[:, :, :3]
    pred = tf.image.resize(pred, size=(256, 256))
    pred = pred / 255.0

    res = int(tf.round(model.predict(x=tf.expand_dims(pred, axis=0))))
    res = "Fire Detected" if res == 0 else "Non Fire Detected"
    title = f"<h2 style='text-align:center'>{res}</h2>"
    st.markdown(title, unsafe_allow_html=True)
    st.image(img, use_column_width=True)

# Title
st.title("Fire Detection")
st.subheader('This app detect fire from given image')

# Image Upload Option
choose = st.selectbox("Select Input Method", ["Upload an Image", "URL from Web"])

if choose == "Upload an Image":  # If user chooses to upload image
    file = st.file_uploader("Upload an image...", type=["jpg", "png", 'Tiff', 'jpeg', 'JPEG', 'JPG', 'PNG'])
    if file is not None:
        img = Image.open(file)
else:  # If user chooses to upload image from url
    url = st.text_area("URL", placeholder="Put URL here")
    if url:
        try:  # Try to get the image from the url
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
        except:  # If the url is not valid, show error message
            st.error(
                "Failed to load the image. Please use a different URL or upload an image."
            )

if img is not None:
    predict = st.button("Predict")
    if predict:
        img_predict(img)