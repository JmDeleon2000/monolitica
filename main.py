import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import plotly.express as px
import pandas as pd


st.title('Monolítico')

def shownegative(img):
    imgInv = ImageOps.invert(img)
    imgInv.save("lastNegative.png")
    
    st.image(imgInv, width=500)
    with open("lastNegative.png", 'rb') as file:
        st.download_button(
                        label=f'Descargar negativo',
                        data=file,
                        file_name=f'negativo.png',
                        mime='text/png',
                    )


uploaded_file = st.file_uploader("Elija un archivo", type=['.png', '.jpg'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, width=500)
    'Elija lo que quiere procesar:'
    negative = st.checkbox('Negativo')
    col1, col2 = st.columns(2)
    with col1:
        do_hists = st.checkbox('Histogramas')
    with col2:
        do_csvs = st.checkbox('Crear CSVs')

    procesar = st.button('Procesar')

    if procesar:
        if negative:
            shownegative(img)

        if do_hists or do_csvs:

            for i, e in enumerate(np.array(img)):
                df = pd.DataFrame()
                df['Red'] =     [j[0] for j in e]
                df['Green'] =   [j[1] for j in e]
                df['Blue'] =    [j[2] for j in e]
                

                if do_hists:
                    fig = px.histogram(df, opacity=0.75)
                    st.plotly_chart(fig)

                if do_csvs:
                    csv = df.to_csv(f'{hex(i)}.csv')
                    with open(f'{hex(i)}.csv', 'rb') as csv:
                        st.download_button(
                            label=f'Descargar {hex(i)}.csv',
                            data=csv,
                            file_name=f'{hex(i)}.csv',
                            mime='text/csv',
                        )


