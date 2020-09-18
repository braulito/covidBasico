"""
Braulio A Firpo Banegas
http://www.lu1aam.com.ar/

Me invitás un cafecito?
https://cafecito.app/lu1aam

"""

import pandas as pd
from shapely import wkt
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image

#CARGO EL DS DE LOS DATOS DE CABA
casos = pd.read_csv("https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/casos-covid-19/casos_covid19.csv")

casos2 = casos

#filtro los registros que son de CABA
casos  = casos[casos['provincia'].isin(['CABA'])] 

#CREO UN CAMPO CON EL TIPO DATETIME 
casos['fechaToma'] =  pd.to_datetime(casos['fecha_toma_muestra'], format='%d%b%Y:%H:%M:%S.%f')

#Ordeno el Dataframe
casos.sort_values(by=['fechaToma'], inplace=True) 

#filtro el DF a partir de la cuarentena
casos = casos[casos['fechaToma'] >= '2020-03-20'] 

#borro las columnas que no necesito
casos.drop(["fecha_apertura_snvs","fecha_clasificacion",
            "fecha_fallecimiento","fallecido",
            "fecha_alta","tipo_contagio",'provincia',
            'comuna','edad','clasificacion',
            'genero','fecha_toma_muestra'],axis=1, inplace=True)  #borro las columnas que no me interesan

#obtengo las FECHAS
fechas = casos['fechaToma'].drop_duplicates()

#EMPIEZO CON LOS BARRIOS
barrios = pd.read_csv("http://cdn.buenosaires.gob.ar/datosabiertos/datasets/barrios/barrios.csv")

#borro las columnas que no necesito
barrios.drop(["comuna","area","perimetro"],axis=1, inplace=True)

#cambio la columna WKT al tipo POLIGONO
barrios['WKT'] = barrios['WKT'].apply(wkt.loads)

#convierto el df barrios a un geodataframe
barrios = gpd.GeoDataFrame(barrios, geometry='WKT')

#contador de gifs
i=0

#defino la carpeta donde voy a guardar los gifs
#CREAR LA CARPETA ANTES!
output_path = 'gif/'

#recorro la serie donde guarde las fechas
for index, value in fechas.items():
    
    #filtro en un df nuevo al df casos con la fecha
    barriosCa = casos[casos['fechaToma'] == value]
    
    #agrupo por barrio
    barriosCa = barriosCa.groupby("barrio")["numero_de_caso"].count()
    barriosCa = barriosCa.to_frame()
    
    #creo un df nuevo con los datos de cada barrio y su poligono
    barriosCa = pd.merge(barrios, barriosCa, on='barrio', how='left')
    
    #relleno de 0 donde 'barrio' es nan
    barriosCa['numero_de_caso'] = barriosCa['numero_de_caso'].fillna(0)
    #dibujo el mapa
    fig = barriosCa.plot(column='numero_de_caso',
                         figsize=(10,10),
                         cmap='Blues',
                         legend=True,
                         linewidth=1,
                         edgecolor='black');
    
    #Configuro el tiulo
    fig.set_title('Tomas realizadas ' + str(value) , 
                  fontdict={'fontsize': '17','fontweight' : '3'})
    
    #configuro pie del grafico
    fig.annotate('Fuente: Datos abiertos GCBA',
                xy=(0.1, .08), xycoords='figure fraction',
                horizontalalignment='left', verticalalignment='top',
                fontsize=10, color='#555555')
    
    #borro los ejes
    fig.axis('off')
    
    
    #GUARDO LOS GRAFICOS EN LA CARPETA GIF
    fi=""
     
    if (i<10) :
        fi = "00" + str(i)
    elif (i<100):
        fi = "0" + str(i)
    else:
        fi = str(i)
    
    filepath = os.path.join(output_path, fi+'.png')
    chart = fig.get_figure()
    chart.savefig(filepath, dpi=72)
    
    #Imprimo estos datos como debug
    print ("Grafico " + str(i) + " fecha " + str(value))
    i = i + 1
    plt.close()
    
#En esta lista guardo los nombres de los archivos que generé
#y guardé en la carpeta gif
frames = []

#leo el directorio
imgs = glob.glob(output_path+"*.png")

#recorro la lista imgs
for i in imgs:
    
    #tomo el archivo
    new_frame = Image.open(i)
    
    #guardo ese nombre
    frames.append(new_frame)

#borro (si es que existe) el gif animado
if os.path.exists('tomasRealizadas.gif'):
        os.remove('tomasRealizadas.gif') 


#creo el gif animado
frames[0].save('tomasRealizadas.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=175, 
               loop=0)   