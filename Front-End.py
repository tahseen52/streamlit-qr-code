import streamlit as st
import pandas as pd
import glob
import base64
from PIL import Image
from io import BytesIO
import os
from Database import Database

result = Database().get_data()

filename = []
details = []
timestamps = []

for i in result:
    filename.append(os.path.join("QR_Code",i[0]))
    details.append(i[1])
    timestamps.append(i[2])

st.button("Refresh")

def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img = img.resize((150, 150))
    return img

def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png') # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'

def link_formatter(link_test: str) -> str:
    return f'<a href= "'+link_test+'">'+link_test+'</a>'


def save_image(image_path: str):
    with open(image_path, 'rb') as file:
        contents = file.read()
        encoded = base64.b64encode(contents).decode()
        href = f'<a href="data:image/jpg;base64,{encoded}" download="{os.path.basename(image_path)}">Download</a>'
        return href
    
@st.cache
def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Image=image_formatter, Decoded_URL = link_formatter, Download_Image = save_image))

st.title('MVP Scanner Data')


df = pd.DataFrame({
                    'image_path': filename,
                    'Image': filename,
                    "Decoded_URL":details ,
                    "TimeStamp": timestamps,
                    "Download_Image":filename },
                index=range(1, len(filename) + 1))

html = convert_df(df)

st.markdown(
    html,
    unsafe_allow_html=True
)
