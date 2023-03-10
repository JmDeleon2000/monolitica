import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import os
import requests


st.title('Monolítico')

def shownegative(uploaded_file, img):
    addr = 'http://stranglerfig-service.labstranglerfig.svc.cluster.local:8000'
    test_url = addr + '/'
    
    with (open('pesimo.fix.meh', 'wb')) as file:
        file.write(uploaded_file.getvalue())
    
    with (open('pesimo.fix.meh', 'rb')) as file:
        my_img = {'image': file}
        response = requests.post(test_url, files=my_img)

    with open('Negativo.png', 'wb') as f:
        f.write(response.content)

    img = Image.open('Negativo.png')
    
    return img, 'Negativo.png'

def createCSV(uploaded_file, img):

    #revisar si el csv ya fue creado
    #crearlo si no ha sido creado o cargarlo si ya existe
    listdir = os.listdir()
    csvname = f'{uploaded_file.name}.csv'
    if not csvname in listdir:
        df = pd.DataFrame()
        for e in np.array(img):
            df['Red'] =     [j[0] for j in e]
            df['Green'] =   [j[1] for j in e]
            df['Blue'] =    [j[2] for j in e]
        df.to_csv(csvname)
    else:
        df = pd.read_csv(csvname)

    return df, csvname


def mandelblend(uploaded_fine, img):
    #computar el set de Mandelbrot
    mandel = Image.effect_mandelbrot(size=img.size, extent=(-2, -2, 2, 2), quality=100)
    alpha = st.slider('Alpha', 0.0, 1.0, 0.5, 0.01)
    #mezclar las dos imágenes
    blendedImage = Image.blend(img, mandel.convert(img.mode), alpha)
    #guardar la imagen nueva
    blendedImage.save(f'{uploaded_file.name}_mandelblend.png')
    return blendedImage

#crear los histogramas y guardarlos como un imagen
def renderHistograms(uploaded_file):
    addr = 'http://stranglerhist-service.labstranglerfig.svc.cluster.local:8000'
    test_url = addr + '/'
    
    with (open('pesimo.fix.meh', 'wb')) as file:
        file.write(uploaded_file.getvalue())
    
    with (open('pesimo.fix.meh', 'rb')) as file:
        my_img = {'image': file}
        response = requests.post(test_url, files=my_img)

    with open('figura.png', 'wb') as f:
        f.write(response.content)

    img = Image.open('figura.png')

    return img, 'figura.png'

uploaded_file = st.file_uploader("Elija un archivo", type=['.png', '.jpg'])

if uploaded_file is not None:

    #Cargar y mostrar la imagen subida por el usuario
    img = Image.open(uploaded_file)
    st.image(img, width=500)

    #Mostrar GUI
    'Elija lo que quiere procesar:'
    negative = st.checkbox('Negativo')
    col1, col2 = st.columns(2)
    with col1:
        do_hists = st.checkbox('Histogramas')
    with col2:
        do_csvs = st.checkbox('Generar .csv de la descomposición de la imagen por colores')
        
    mandelbrot = st.checkbox('Superponer el set de mandelbrot')
    procesar = st.button('Procesar')

    if procesar:
        if negative:
            imgInv, negativeName = shownegative(uploaded_file, img)
            #mostrar el negativo junto con el botón de descarga
            st.image(imgInv, width=500)
            with open(negativeName, 'rb') as file:
                st.download_button(
                        label=f'Descargar negativo',
                        data=file,
                        file_name=negativeName,
                        mime='text/png',
                    )

        if do_hists or do_csvs:
            df, csvname = createCSV(uploaded_file, img)

            if do_hists:
                fig, fig_name = renderHistograms(uploaded_file)
                st.pyplot(fig)
                with open(fig_name, 'rb') as file:
                    st.download_button(
                            label=f'Descargar Histogramas',
                            data=file,
                            file_name=fig_name,
                            mime='text/png',
                        )
            if do_csvs:
                df
                with open(csvname, 'rb') as csv:
                    st.download_button(
                label=f'Descargar {csvname}',
                data=csv,
                file_name=csvname,
                mime='text/csv',
                )   

    if mandelbrot:
        #extraer la función
        blendedImage = mandelblend(uploaded_file, img)

        #no el GUI que muestra la imagen y permite descargarla
        st.image(blendedImage, width=500)
        with open(f'{uploaded_file.name}_mandelblend.png', 'rb') as file:
            st.download_button(
                            label=f'Descargar',
                            data=file,
                            file_name=f'{uploaded_file.name}_mandelblend.png',
                            mime='text/png',
                        )