# Aplicación desarrollada en Streamlit para la visualización de las observaciones de especies de triatomine americano.
# Autor: Jorge Guillermo Rodriguez Herrera (El Memo de Mileto https://github.com/Memo1986)
# Fecha de creación: 04-01-2024

## Importar pandas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt # biblioteca de graficación
## import calendar # biblioteca para manejo de fechas
import os
import requests
import zipfile
import contextily as cx
from geojson import dump
from owslib.wfs import WebFeatureService
from mpl_toolkits.axes_grid1 import make_axes_locatable
import descartes
import folium
from folium import Marker
import math
import plotly.express as px
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from streamlit_folium import folium_static

## Importar pandas
import streamlit as st

st.title("Ejemplo de aplicación Streamlit")

#
# Título y descripción de la aplicación
#

st.title("Visualización de observaciones de triatomine americano")
st.markdown("Esta aplicación presenta tabuladores, gráficas y datos geoespaciales de la especie de triatomine americano")
st.markdown("El usuario deb seleccionar un archivo .csv")
st.markdown("La aplicación mostrará un conjunto de salidas en forma de tablas, gráficas y mapas")

