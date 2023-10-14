import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

#cargamos datos de la base de datos
df = pd.read_csv('who_suicide_statistics.csv') 

#retiramos valores nulos de cualquier columna
df = df.dropna()

#filtramos rango de edad de 20 años para tener buen dataset
df = df[(df["year"] >= 1990) & (df["year"] <= 2010)]

#nos quitamos valores con menos de 100 datos para cada país
df = df[~df['country'].isin(df['country'].value_counts()[df['country'].value_counts() < 100].index)]

# mejoramos el rendimiento de los datos
df = df.copy()
df['year'] = df['year'].astype("int16")
df['suicides_no'] = df['suicides_no'].astype("int16")
df['population'] = df['population'].astype("int32")
df['country'] = df['country'].astype("string")
df['sex'] = df['sex'].astype("string")

# calculamos el valor de los suicidios por cada 100000 habitantes
data = {'suicides', 'population'}
def calcular_porcentaje_suicidios(row):
    return (row['suicides_no'] / row['population']) * 100000
df['Suicidios x100000'] = df.apply(calcular_porcentaje_suicidios, axis=1)

# limpiamos datos para prevenir errores
df['country'] = df['country'].replace('\(USA\)','', regex = True)
df['country'] = df['country'].replace('\(Bolivarian Republic of\)','', regex = True)

# organizamos una columna para clasificar continentes: 
europa = ['Ukraine', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Sweden', 'Spain', 'Romania', 'Russian Federation', 'Slovenia', 'Germany', 'France', 'Belgium', 'Czech Republic', 'Bulgaria', 'Estonia', 'United Kingdom', 'Finland', 'Austria', 'TFYR Macedonia', 'Poland', 'Albania', 'Slovakia', 'Portugal', 'Belarus','Denmark','Switzerland','Azerbaijan','Croatia', 'Serbia', 'Montenegro', 'Cyprus']
america = ['Guatemala','Trinidad and Tobago','Mexico','Puerto Rico','United States of America','Colombia','Costa Rica', 'Chile','Canada','Ecuador','Brazil','Argentina','Saint Lucia','Guyana','El Salvador','Belize','Suriname', 'Venezuela ', 'Paraguay', 'Cuba', 'Uruguay','Bahamas','Antigua and Barbuda','Saint Vincent and Grenadines','Barbados','Grenada','Panama', 'Virgin Islands ', 'Aruba', 'Martinique', 'Jamaica', 'Guadeloupe', 'French Guiana', 'Reunion']
africa = ['South Africa', 'Egypt', 'Seychelles']
asia = ['Hong Kong SAR','Israel','Japan','Kazakhstan','Kyrgyzstan','Republic of Korea','Republic of Moldova','Singapore','Turkmenistan','Armenia','Thailand','Uzbekistan','Kuwait', 'Brunei Darussalam', 'Mauritius', 'Georgia', 'Philippines', 'Bahrain', 'Qatar', 'Sri Lanka', 'Maldives']
oceania = ['New Zealand','Australia', 'Kiribati', 'Fiji']
df["continent"] = df["country"]
df['continent'] = df['continent'].replace(europa,'Europa', regex = True)
df['continent'] = df['continent'].replace(america,'America', regex = True)
df['continent'] = df['continent'].replace(africa,'Africa', regex = True)
df['continent'] = df['continent'].replace(asia,'Asia', regex = True)
df['continent'] = df['continent'].replace(oceania,'Oceania', regex = True)
df = df.reindex(columns=['country', 'continent','year', 'sex', 'age', 'suicides_no', 'population','Suicidios x100000'])

#guardamos los datos limpios a un nuevo .csv
df_l = df.to_csv('datos_limpios.csv')


'''organizamos un mapa para visualizar los datos por rango de
edad y de sexos
'''
num_intentos = 3

for intento in range(num_intentos):
    age_range = int(input("Introduce el rango de edad a filtrar:\n1. 5-14 years\n2. 15-24 years\n3. 25-34 years\n4. 35-54 years\n5. 55-74 years\n6. 75+ years\n"))

    if age_range == 1:
        age_range = "5-14 years"
    elif age_range == 2:
        age_range = "15-24 years"
    elif age_range == 3:
        age_range = "25-34 years"
    elif age_range == 4:
        age_range = "35-54 years"
    elif age_range == 5:
        age_range = "55-74 years"
    elif age_range == 6:
        age_range = "75+ years"
    else:
        print("Valor no válido. Intento {}/{}.".format(intento, num_intentos))
        if intento == num_intentos:
            print("Has agotado tus 3 intentos. Saliendo del programa.")
        continue
    break  # Rompe el bucle si la entrada es válida


max_intentos = 3

for intento in range(1, max_intentos + 1):
    sex_fm = int(input("Introduce el sexo a filtrar:\n1. female\n2. male\n"))

    if sex_fm == 1:
        sex_fm = "female"
    elif sex_fm == 2:
        sex_fm = "male"
    else:
        print("Valor no válido. Intento {}/{}.".format(intento, max_intentos))
        if intento == max_intentos:
            print("Has agotado tus 3 intentos. Saliendo del programa.")
        continue
    break  # Rompe el bucle si la entrada es válida

print(f"Seleccionado el rango de edad: {age_range}")
print(f"Seleccionado el sexo a filtrar: {sex_fm}")

df_pers = df.loc[(df["age"]==age_range) & (df["sex"]==sex_fm), :]#.drop(["sex", "age", "suicides_no", "population"], axis=1)
df_pers = df_pers.groupby(['country','continent'])['Suicidios x100000'].sum()
df_pers = pd.DataFrame(df_pers).reset_index()

import json

with open("world_countries.json", 'r') as f:
  world_geo=json.load(f)

world_map = folium.Map(location=[0, 0], zoom_start=3)

world_map.choropleth(
    geo_data=world_geo,
    data=df_pers,
    columns=['country', "Suicidios x100000"],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Suicidios por 100000 habitantes'
)

# mostramos el mapa
world_map








