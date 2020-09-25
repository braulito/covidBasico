"""
Braulio A Firpo Banegas
http://www.lu1aam.com.ar/

Me invitás un cafecito?
https://cafecito.app/lu1aam

"""

import pandas as pd
import matplotlib.pyplot as plt

#CARGO EL DS DE LOS DATOS DE CABA
casos = pd.read_csv("https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/casos-covid-19/casos_covid19.csv")

#filtro los registros que son de CABA
casos  = casos[casos['provincia'].isin(['CABA'])] 

#CREO UN CAMPO CON EL TIPO DATETIME 
casos['fechaToma'] =  pd.to_datetime(casos['fecha_toma_muestra'], format='%d%b%Y:%H:%M:%S.%f')

#Ordeno el Dataframe
casos.sort_values(by=['fechaToma'], inplace=True) 

#filtro el DF a partir de la cuarentena
casos = casos[casos['fechaToma'] >= '2020-03-20'] 

#filtro a los confirmados
casos = casos[casos['clasificacion'] == 'confirmado'] 

#borro las columnas que no necesito
casos.drop(["fecha_apertura_snvs",'clasificacion',
            'fecha_toma_muestra',
            'fecha_clasificacion','tipo_contagio',
            'provincia','barrio','comuna',
            'fecha_alta','fecha_fallecimiento',
            'fallecido'],axis=1, inplace=True)

#limpio las filas donde genero o edad no haya sido cargadoo
casos = casos[casos['edad'].notnull()]
casos = casos[casos['genero'].notnull()]

#ordeno por edad
casos.sort_values(by=['edad'], inplace=True)

#Obtengo los valores del eje VERTICAL
casos['grupoEtario'] = pd.cut(x=casos['edad'], 
                              bins=[-1,10, 20, 30, 40,50,
                                    60,70,80,90,100,110,120],
                              labels=['0 a 10','11 a 20','21 a 30',
                                      '31 a 40','41 a 50','51 a 60',
                                      '61 a 70','71 a 80','81 a 90',
                                      '91 a 100','101 a 110','111 a 120'])



#trabajo para conseguir los valores de cada sexo
casosFem = casos[(casos['genero'] == 'femenino') ].groupby("grupoEtario")["numero_de_caso"].count()
casosHom = casos[(casos['genero'] == 'masculino')].groupby("grupoEtario")["numero_de_caso"].count()

#variable para calcular el corrimiento entre las barras
corrimiento = 0

#Creo los cuartiles para el eje HORIZONTAL
cuartiles = []

if (casosHom.max() > casosFem.max()):
    cuartiles.append(int(casosHom.describe()['25%']))
    cuartiles.append(int(casosHom.describe()['50%']))
    cuartiles.append(int(casosHom.describe()['75%']))
    cuartiles.append(int(casosHom.describe()['max']))
    corrimiento = int(casosHom.values.max())
else:
    cuartiles.append(int(casosFem.describe()['25%']))
    cuartiles.append(int(casosFem.describe()['50%']))
    cuartiles.append(int(casosFem.describe()['75%']))
    cuartiles.append(int(casosFem.describe()['max']))
    corrimiento = int(casosFem.values.max())
    
corrimiento = int(corrimiento/80)

#consigo losvalores eje VERTICAL
x = list(range(0, len(casos['grupoEtario'].unique())))

tick_lab = [cuartiles[3],cuartiles[2],cuartiles[1],cuartiles[0],
            cuartiles[0],cuartiles[1],cuartiles[2],cuartiles[3]]
tick_val = [-cuartiles[3]-corrimiento,-cuartiles[2]-corrimiento,-cuartiles[1]-corrimiento,-cuartiles[0]-corrimiento,
            cuartiles[0]+corrimiento,cuartiles[1]+corrimiento,cuartiles[2]+corrimiento,cuartiles[3]+corrimiento]

plt.figure(figsize=(20,10))

h = plt.barh(x, -casosHom, height=.75,left=-corrimiento, align='center' , color="deepskyblue")
m = plt.barh(x, casosFem, height=.75,left=corrimiento, align='center', color="pink")

plt.legend([h,m], ['Hombres','Mujeres'])
plt.yticks(x, casos['grupoEtario'].unique())
plt.xticks(tick_val, tick_lab)
plt.grid(b=False)
plt.title("Casos confirmados de Covid 19 por edad y sexo")
plt.show()
plt.close()

