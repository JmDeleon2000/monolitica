import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import plotly.express as px
import pandas as pd
import os


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
        do_csvs = st.checkbox('Quiero descargar un .csv')

    procesar = st.button('Procesar')

    if procesar:
        if negative:
            shownegative(img)

        listdir = os.listdir()
        if do_hists or do_csvs:

            for i, e in enumerate(np.array(img)):
                csvname = f'{uploaded_file.name}_{hex(i)}.csv'
                if not csvname in listdir:
                    df = pd.DataFrame()
                    df['Red'] =     [j[0] for j in e]
                    df['Green'] =   [j[1] for j in e]
                    df['Blue'] =    [j[2] for j in e]
                    df.to_csv(csvname)
                else:
                    df = pd.read_csv(csvname)

                if do_hists:
                    fig = px.histogram(df, opacity=0.75, nbins=20)
                    st.plotly_chart(fig)

                if do_csvs:
                    with open(csvname, 'rb') as csv:
                        st.download_button(
                            label=f'Descargar {csvname}',
                            data=csv,
                            file_name=csvname,
                            mime='text/csv',
                        )


