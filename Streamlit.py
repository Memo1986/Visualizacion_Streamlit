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
# from geojson import dump
# from owslib.wfs import WebFeatureService
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# import descartes
import folium
from folium import Marker
import math
import plotly.express as px
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import fiona
#import matplotlib
# import matplotlib.pyplot as plt # biblioteca de graficación




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
registros_arriba = st.file_uploader("Seleccione el archivo .CSV, que contiene las observaciones de triatomine americano")


# Se continua con precesamiento de los datos solo si hya un archivo de datos cargado
if registros_arriba is not None:
    # Cargar de registro de presencia de triatomine americano en un data frame
    registros = pd.read_csv(registros_arriba)
    # Conversión del data frame de presencia a geodataframe
    registros_presencia = gpd.GeoDataFrame(registros,
                                           geometry = gpd.points_from_xy(registros.decimalLongitude,
                                                                         registros.decimalLatitude),
                                                                         crs = "EPSG:4326")



# Cargar los polígonos del continente Americano
ame = gpd.read_file("C:/Users/Memo/Desktop/PF-3311/Clase_07/Visualizacion_Streamlit/Datos/America.shp")


# Limpieza de datos
# Eliminación de registros con valores nulos en la columna "scientificName"
registros_presencia = registros_presencia[registros_presencia["scientificName"].notna()]
# Eliminación de registros con valores nulos en la columna "scientificName"
registros_fecha = registros_presencia[registros_presencia["year"].notna()]
registros_fecha.year = registros_fecha.year.astype("int")
registros_fecha["Year_01"] = registros_fecha.year.astype("str")
# reg_fecha = registros_fecha[["id",'scientificName',"decimalLatitude", 
#                               "decimalLongitude", "collectionCode",'eventDate', 'year', 'month','country', "ID_Serie","Year_01"]]
# registros_fecha["year"] = pd.to_datetime[registros_fecha["year"]]
# Eliminar las coordenadas repetidas
datos_00 = registros_fecha.drop_duplicates(['decimalLatitude', 'decimalLongitude'], keep='last')
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


st.header("Filtros por Año")
# Listas
lista_year = registros_fecha.Year_01.unique().tolist()
lista_year.sort()
filtro_year = st.selectbox("Seleccione un año", lista_year)	

# Procesamiento

# Filtrado
registros_presencia_0 = registros_fecha[registros_fecha["scientificName"] == filtro_especie]
# Union espacial de las depas de America y registros de presencia
ame_registros = ame.sjoin(registros_presencia_0, how = "left", predicate = "contains")
# Conteo de resgistros de presencia en cada pais
ame_reg_count = ame_registros.groupby("country").agg(cantidad_registros = ("scientificName", "count"))
ame_reg_count = ame_reg_count.reset_index()

registros_presencia_1 = registros_presencia[registros_presencia["country"] == filtro_pais]
# Union espacial de las depas de America y registros de presencia
ame_reg_pais = ame.sjoin(registros_presencia_1, how = "left", predicate = "contains")
# Conteo de resgistros de presencia en cada pais
ame_reg_pais= ame_reg_pais.groupby("country").agg(cantidad_registros = ("scientificName", "count"))
ame_reg_pais = ame_reg_pais.reset_index()

registros_presencia_2 = registros_fecha[registros_fecha["Year_01"] == filtro_year]
# Cambio de fecha
# Remplazar los NaN por la cadena string de 1000
# fecha = datos_01[datos_01["year"].notna()]
# # fecha = fecha.year.fillna('1000', inplace = True) 
# # # Seleccionar de la columna year los ultimos 4 caracteres y agregarlo a la nueva columna de Year_0
# fecha["Year_0"] = fecha["year"].str[-4:]
# # # Remplazar los NaN por 1000
# fecha.Year_0.fillna('1000', inplace = True) 
# # # Cambiar el tipo de a columna de Year_0 (object) a int
# #fecha.Year_0 = fecha.Year_0.astype("int")
# # # Seleccionar los datos mayotes a 1000
# fecha_0 = fecha[fecha["Year_0"] > 1000]
# # # Agrupar los datos por año
# fecha_01 = fecha_0.groupby('Year_0').count()
# # # Agregarle un índice al nuevo dataframe
# fecha_01 = fecha_01.reset_index()
# # 
# # fecha_0.Year_0 = fecha_0.Year_0.astype("str")


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
st.dataframe(registros_presencia_0[['scientificName',"decimalLatitude",  
                              "decimalLongitude", 'eventDate','country']].rename(
    columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud",
              "decimalLongitude": "Longitud",
              'eventDate': "Fecha", "country": "Pais"}))
st.write("Cantidad total de observaciones de ", filtro_especie, "es = ", len(registros_presencia_0))

# Tabla de registros por pais
st.header("Tabla de registros de presencia en " + filtro_pais)
st.subheader("st.dataframe()")
st.dataframe(registros_presencia_1[['scientificName', "decimalLatitude",  "decimalLongitude", 'country']].rename(
    columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud","decimalLongitude": "Longitud",
              "country": "Pais"}))
st.write("Cantidad total de observaciones de triatomine americano en ", filtro_pais, "es = ", len(registros_presencia_1))


st.header("Tabla de registros de triatomine americano en " + filtro_year)
st.subheader("st.dataframe()")
st.dataframe(registros_presencia_2[['scientificName', "decimalLatitude",  "decimalLongitude", 'country', "Year_01"]].rename(
    columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud","decimalLongitude": "Longitud",
              "Year_01": "Fecha", "country": "Pais"}))


# Tabla de registros por year
# st.header("Tabla de registros de presencia por año " + str(filtro_year))
# # st.header("Cantidad de observaciones ", cantidad)
# # st.header("Cantidad de observaciones 0", len(filtro_especie))
# st.subheader("st.dataframe()")
# st.dataframe(registros_presencia_1[['scientificName',"decimalLatitude",  
#                               "decimalLongitude", 'Year_0','country']].rename(
#     columns= {'scientificName': "Nombre Científico", "decimalLatitude": "Latitud",
#               "decimalLongitude": "Longitud",
#               'Year_0': "Year", "country": "Pais"}))




# Datos espaciales
# Convertir a GeoDataFrame
# triatoma_0 = gpd.GeoDataFrame(resgistros_presencia, geometry=gpd.points_from_xy(datos_00.decimalLongitude, datos_00.decimalLatitude),
#                               crs = "EPSG:4326")
# # Reaizar una intersección 
# triatoma_interc = triatoma_0.overlay(ame, how="intersection")


# Graficos de tiempo
st.header("Gráfico de presencia de triatomine americano por año " + filtro_especie)
datatri_07 = registros_presencia_0.loc[:, ['scientificName', "Year_01"]]
datatri_07
pres_year = pd.DataFrame(datatri_07.groupby(datatri_07["Year_01"]).count())
# pres_year.columns = ["Observacion_Anual"]
st.subheader("st.bar_chart()")
st.bar_chart(pres_year)

#PLotear
st.subheader("px.bar()")
fig = px.bar(pres_year,
             labels = {"Year_01": "Año", "value":"Registros de presencia"},
             title = "Historial de resgistros de presencia por año de " + filtro_especie )
st.plotly_chart(fig)

 
# Graficos de tpais
st.header("Gráfico de presencia de triatomine americano por Pais " + filtro_especie)
st.write(ame_reg_pais)






























