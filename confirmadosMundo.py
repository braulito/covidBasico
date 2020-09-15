import pandas as pd

listaPaises = ['Argentina','Brazil','Chile','Germany','Italy','Spain','Uruguay']

confirmados = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

confirmados.drop(["Province/State","Lat","Long"],axis=1, inplace=True)

confirmados  = confirmados[confirmados['Country/Region'].isin(listaPaises)]

confirmados.rename(columns = {'Country/Region': 'País'}, inplace = True)
co = confirmados
confirmados.set_index('País', inplace=True)

confirmados = confirmados.transpose()

habitantes = [44490000,209500000,18730000,83020000,60360000,46940000,3449000]

confirmados['Argentina'] = confirmados['Argentina']*1000000/habitantes[0]
confirmados['Brazil'] = confirmados['Brazil']*1000000/habitantes[1]
confirmados['Chile'] = confirmados['Chile']*1000000/habitantes[2]
confirmados['Germany'] = confirmados['Germany']*1000000/habitantes[3]
confirmados['Italy'] = confirmados['Italy']*1000000/habitantes[4]
confirmados['Spain'] = confirmados['Spain']*1000000/habitantes[5]
confirmados['Uruguay'] = confirmados['Uruguay']*1000000/habitantes[6]


confirmados.plot(figsize=(10,7),
                 title='Casos confirmados por millón de habitantes',
                 xlabel='Fecha',
                 ylabel='Casos')

