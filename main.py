import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import plotly.express as px
import pandas as pd
import os
from time import sleep


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

def histAndCsv(uploaded_file, img):
    listdir = os.listdir()
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
        
    
    mandelbrot = st.checkbox('Superponer el set de mandelbrot')

    procesar = st.button('Procesar')

    if procesar:
        if negative:
            shownegative(img)

        if do_hists or do_csvs:
            histAndCsv(uploaded_file, img)
    

        
    if mandelbrot:
        mandel = Image.effect_mandelbrot(size=img.size, extent=(-2, -2, 2, 2), quality=100)
        alpha = st.slider('Alpha', 0.0, 1.0, 0.5, 0.01)
        blendImage = Image.blend(img, mandel.convert(img.mode), alpha)
        blendImage.save(f'{uploaded_file.name}_mandelblend.png')
        st.image(blendImage, width=500)
        with open(f'{uploaded_file.name}_mandelblend.png', 'rb') as file:
            st.download_button(
                            label=f'Descargar',
                            data=file,
                            file_name=f'{uploaded_file.name}_mandelblend.png',
                            mime='text/png',
                        )





