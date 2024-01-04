## Importar pandas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt # biblioteca de graficación
# % matplotlib inline
import calendar # biblioteca para manejo de fechas
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
import streamlit as st


st.title("Ejemplo de aplicación Streamlit")