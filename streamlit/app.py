import streamlit as st
import requests
import io
import PIL.Image

st.title('Plant Disease Identification')

image = st.file_uploader('Please upload your image', type=['png', 'jpg', 'jpeg'])

if image is not None:
    img = PIL.Image.open(image)
    st.image(img, caption='Uploaded Image', use_column_width=False)

    button = st.button('Identify')

    if button:
        img_as_byte = io.BytesIO()
        img.save(img_as_byte, format='PNG')
        img_byte_arr = img_as_byte.getvalue()

        response = requests.post('http://localhost:8000/analysis', files={"file": img_byte_arr})
        response.raise_for_status()

        result = response.json()
        st.markdown(f"**Prediction:** {result['prediction']}")
        st.markdown(f"**Confidence:** {round(result['confidence'], 2)}")
