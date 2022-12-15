import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import plotly.express as px
import pandas as pd


st.title('FiltrosFacil')
original = st.checkbox('Original', value=True)
negative = st.checkbox('Negativo')
do_hists = st.checkbox('Histogramas')

uploaded_file = st.file_uploader("Elija un archivo", type=['.png', '.jpg'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if original:
        st.image(img, width=500)
    if negative:
        imgInv = ImageOps.invert(img)
        st.image(imgInv, width=500)

    if do_hists:
        
        for i, e in enumerate(np.array(img)):
            df = pd.DataFrame()
            df['Red'] =     [j[0] for j in e]
            df['Green'] =   [j[1] for j in e]
            df['Blue'] =    [j[2] for j in e]
            fig = px.histogram(df, opacity=0.75)

            st.plotly_chart(fig)

            csv = df.to_csv().encode('utf-8')
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f'{hex(i)}.csv',
                mime='text/csv',
            )


