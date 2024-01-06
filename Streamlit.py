# Aplicación desarrollada en Streamlit para la visualización de las observaciones de especies de triatomine americano.
# Autor: Jorge Guillermo Rodriguez Herrera (El Memo de Mileto https://github.com/Memo1986)
# Fecha de creación: 04-01-2024

## Importar pandas
import streamlit as st
import pandas as pd 
import geopandas as gpd
import numpy as np
import calendar # biblioteca para manejo de fechas
import os
import requests
import zipfile
# import contextily as cx
from geojson import dump
# from owslib.wfs import WebFeatureService
# from mpl_toolkits.axes_grid1 import make_axes_locatable
import descartes
import folium
from folium import Marker
import math
import plotly.express as px
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib
import matplotlib.pyplot as plt # biblioteca de graficación




st.title("Ejemplo de aplicación en Streamlit")

#
# Título y descripción de la aplicación
#

st.title("Visualización de observaciones de triatomine americano")
st.markdown("Esta aplicación presenta tabuladores, gráficas y datos geoespaciales de la especie de triatomine americano")
st.markdown("El usuario deb seleccionar un archivo .csv")
st.markdown("La aplicación mostrará un conjunto de salidas en forma de tablas, gráficas y mapas")

#
# Entradas
#

# Cargar los datos
st.header("Cargar los datos")
registros = st.file_uploader("Seleccione el archivo .CSV, que contiene las observaciones de triatomine americano")


# Se continua con precesamiento de los datos solo si hya un archivo de datos cargado
if registros is not None:
    # Cargar de registro de presencia de triatomine americano en un data frame
    registros = pd.read_csv(registros)
    # Conversión del data frame de presencia a geodataframe
    registros_presencia_0 = gpd.GeoDataFrame(registros, 
                                            geometry = gpd.points_from_xy(registros.decimalLongitude,
                                                                         registros.decimalLatitude),
                                                                         crs = "EPSG:4326")



# Cargar los polígonos del continente Americano
ame = gpd.read_file("C:/Users/Memo/Desktop/PF-3311/Clase_06/Datos/America.shp")


# Limpieza de datos
# Eliminación de registros con valores nulos en la columna "scientificName"
registros_0 = registros_presencia_0[registros_presencia_0["scientificName"].notna()]
# Eliminar las coordenadas repetidas
datos_00 = registros_0.drop_duplicates(['decimalLatitude', 'decimalLongitude'], keep='last')
# Despliegue de las columnas con el nombre científico, la especie, la fecha, el año, el mes y el día
datos_01 = datos_00[["id",'scientificName',"decimalLatitude", 
                              "decimalLongitude", "collectionCode",'eventDate', 'year', 'month','country', "ID_Serie"]]


# Especificación de listas
st.header("Filtros por nombre científico")
# Listas
lista_especies = datos_01.scientificName.unique().tolist()
lista_especies.sort()
filtro_especie = st.selectbox("Seleccione la especie", lista_especies)	


st.header("Filtros por pais")
# Listas
lista_pais = datos_01.country.unique().tolist()
lista_pais.sort()
filtro_pais = st.selectbox("Seleccione un pais", lista_pais)	




# Procesamiento

# Filtrado
registros_presencia_1 = registros_presencia_0[registros_presencia_0["scientificName"] == filtro_especie]
# Union espacial de las depas de America y registros de presencia
ame_registros = ame.sjoin(registros_presencia_1, how = "left", predicate = "contains")
# Conteo de resgistros de presencia en cada pais
ame_reg_count = ame_registros.groupby("country").agg(cantidad_registros = ("scientificName", "count"))
ame_reg_count = ame_reg_count.reset_index()

registros_presencia_2 = registros_presencia_0[registros_presencia_0["country"] == filtro_pais]
# Union espacial de las depas de America y registros de presencia
ame_reg_pais = ame.sjoin(registros_presencia_2, how = "left", predicate = "contains")
# Conteo de resgistros de presencia en cada pais
ame_reg_pais= ame_reg_pais.groupby("country").agg(cantidad_registros = ("scientificName", "count"))
ame_reg_pais = ame_reg_pais.reset_index()


# Cambio de fecha
# Remplazar los NaN por la cadena string de 1000
# fecha = datos_01.year.fillna('1000', inplace = True) 
# # Seleccionar de la columna year los ultimos 4 caracteres y agregarlo a la nueva columna de Year_0
# fecha["Year_0"] = fecha["year"].str[-4:]
# # Remplazar los NaN por 1000
# fecha.Year_0.fillna('1000', inplace = True) 
# # Cambiar el tipo de a columna de Year_0 (object) a int
# fecha.Year_0 = fecha.Year_0.astype("int")
# # Seleccionar los datos mayotes a 1000
# fecha_0 = fecha[fecha["Year_0"] > 1000]
# # Agrupar los datos por año
# fecha_01 = fecha_0.groupby('Year_0').count()
# # Agregarle un índice al nuevo dataframe
# fecha_01 = fecha_01.reset_index()


# Cambio del tipo de datos del campo fecha
# datatri_02 = resgistros_presencia.loc[:, ['country', 'scientificName']]
# # Cambiar el nombre de las columnas
# datatri_02 = datatri_02.rename(columns={'country':'País',
#                                    'scientificName':'Observación'})
# # Agrupar por pais
# datatri_03 = datatri_02.groupby("País").count()
# # Estilo de los gráficos
# plt.style.use('ggplot')
# # Plotear los datos 
# datatri_03.plot(kind = "barh", width=0.8
#                 , color={"green"} )


# Salidas

# Tabla de registros de presencia 
st.header("Tabla de registros de presencia por nombre científico " + filtro_especie)
# Cantidad
cantidad = len(filtro_especie)
# st.header("Cantidad de observaciones ", cantidad)
# st.header("Cantidad de observaciones 0", len(filtro_especie))
st.subheader("st.dataframe()")
st.dataframe(registros_presencia_1[['scientificName',"decimalLatitude",  
                              "decimalLongitude", 'eventDate','country']].rename(
    columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud",
              "decimalLongitude": "Longitud",
              'eventDate': "Fecha", "country": "Pais"}))


# Tabla de registros por pais
st.header("Tabla de registros de presencia por pais " + filtro_pais)
st.subheader("st.dataframe()")
st.dataframe(registros_presencia_2[['scientificName', "decimalLatitude",  "decimalLongitude", 'country']].rename(
    columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud","decimalLongitude": "Longitud",
              "country": "Pais"}))

# Datos espaciales
# Convertir a GeoDataFrame
# triatoma_0 = gpd.GeoDataFrame(resgistros_presencia, geometry=gpd.points_from_xy(datos_00.decimalLongitude, datos_00.decimalLatitude),
#                               crs = "EPSG:4326")
# # Reaizar una intersección 
# triatoma_interc = triatoma_0.overlay(ame, how="intersection")


































