import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import pandas as pd
import os


st.title('Monolítico')

def shownegative(uploaded_file, img):
    #crear el negativo de la imagen
    imgInv = ImageOps.invert(img)
    #generar un nombre interno y público para el negativo
    negativeName = f'{uploaded_file.name}_negativo.png'
    #guardar el negativo con ese nombre
    imgInv.save(negativeName)
    
    return imgInv, negativeName

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
def renderHistograms(df):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.hist(df['Red'],     bins=20, color='red'    )
    ax2.hist(df['Green'],   bins=20, color='green'  )
    ax3.hist(df['Blue'],    bins=20, color='blue'   )
    ax1.set_title('Rojo')
    ax2.set_title('Verde')
    ax3.set_title('Azul')

    fig.tight_layout()
    fig_name = f'{uploaded_file.name}_fig.png'
    plt.savefig(fig_name)
    return fig, fig_name

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
                fig, fig_name = renderHistograms(df)
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