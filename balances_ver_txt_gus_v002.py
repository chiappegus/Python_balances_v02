# -*- coding: utf-8 -*-
"""BALANCE_TXT_GUS_V02.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YHr13Ay4LprMENKnk2kSbU2I7OU6TIYF

## Importando datos
"""

import pandas as pd
import numpy as np
from datetime import date

df1 = pd.read_csv('balances.txt', sep=',')

# df1['sum'] = df1[["M2.1","M2.2"]].sum(axis=1)
# print(df1['sum'] )
#df1.replace(,12)

df1=df1.fillna(np.nan)

#df1=df1.replace("",np.nan)
# df1=df1.fillna(0)

# df1['S1'] = df1[["S1-III","S1-IV","S1-V","S1-VII"]].sum(axis=1,numeric_only=True)
# df1['S2'] = df1[["TS(S2)III","TS(S2)IV","TS(S2)V","TS(S2)VI"]].sum(axis=1,numeric_only=True)

df1['S1'] = df1[["S1-III","S1-IV","S1-V","S1-VII"]].sum(axis=1, min_count=1)
df1['S2'] = df1[["TS(S2)III","TS(S2)IV","TS(S2)V","TS(S2)VI"]].sum(axis=1, min_count=1)



# df1["S1"]=+df1["S1-III"]+df1["S1-IV"]+df1["S1-V"]+df1["S1-VII"]
# df1["S2"]=+df1["TS(S2)III"]+df1["TS(S2)IV"]+df1["TS(S2)V"]+df1["TS(S2)VI"]

df1=df1.drop(columns={"S1-III","S1-IV","S1-V","S1-VII","TS(S2)III","TS(S2)IV","TS(S2)V","TS(S2)VI","CoordX","CoordY"})
# df1.head()

df1["M1"]=df1["M1.2"]
df1["M2"]=df1["M2.2"]

# Reemplazar valores en "M1" si "M1.2" es NaN con el valor de "M1.1"
df1.loc[pd.isna(df1["M1.2"]), "M1"] = df1["M1.1"]

# Reemplazar valores en "M1" si "M1.2" es NaN con el valor de "M1.1"
df1.loc[pd.isna(df1["M2.2"]), "M2"] = df1["M2.1"]
# df1["M2"][(df1["M2"]== 0) & (df1["M2.1"]>0)]=df1["M2.1"]
# df1["M2"][(df1["M2"]==np.nan) & (df1["M2.1"]!=np.nan)]=df1["M2.1"]
# df2 = df1[["M1","M1.2","M1.1","M2","M2.2","M2.1"]].copy()

nueva_fila = []

for i in range(len(df1.columns)):
    if i == 0:  # Si es la primera columna
        #nueva_fila.append(np.nan)
        nueva_fila.append("NA")

    else:  # Las columnas restantes
        nueva_fila.append(-2000)

df1.loc[len(df1)]=nueva_fila

df1=df1.drop(columns={"M1.1","M1.2","M2.1","M2.2"})
# df1

# df2.head()

# df1.head()
 
# Renaming columns
df1.rename(columns={'G1.1': 'G1', 'G1.2': 'G2','A1.1':'A1','A1.2':'A2','TS(TC)':'TC'}, inplace=True)
# print(df1.head())

#otro
# Reemplazar valores en "M1" si "M1.2" es NaN con el valor de "M1.1"
df1.loc[pd.isna(df1["P"]), "P"] = df1["CN"]
#df1["P"][df1["P"]==0]=df1["CN"]
df1=df1.drop(columns={"CN"})
# print(df1.head())

df1.loc[pd.isna(df1["TL"]), "TL"] = df1["TS(TL)"]
df1=df1.drop(columns={"TS(TL)"})
# print(df1.head())

# df1=df1.fillna(-1000)
#df1=df1.replace(0,-1000)
df1=df1.fillna(-1000)
# print(df1.head())

todays_date = date.today()
# print("Today's date =", todays_date)
df1.to_excel(f"balances_GUS_{todays_date}.xlsx",index=False)

"""##CARGA DE SHP  ##

### probando con shp de

###instalar el geoPandas
"""

#%pip install geopandas
#%pip install geodatasets

import geopandas as gpd
from geodatasets import get_path
import os
import zipfile

# path_to_data = get_path("nybb")
# gdf = geopandas.read_file(path_to_data)

# gdf

#path_to_data
#'C:\\Users\\gchiappe\\AppData\\Local\\geodatasets\\geodatasets\\Cache\\nybb_16a.zip.unzip\\nybb_16a\\nybb.shp'

"""## preparacion de Carpetas"""

import shutil

data_folder = 'reservas'
output_folder = 'output'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)


# Eliminar la carpeta
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
    print(f"La carpeta {output_folder} ha sido eliminada")
else:
    print("La carpeta no existe")



if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# data_folder = 'reservas'
# output_folder = 'output'

# if not os.path.exists(data_folder):
#     os.mkdir(data_folder)
# if not os.path.exists(output_folder):
#     os.mkdir(output_folder)

"""### RESERVAS"""

reservasshp = os.path.join(data_folder, 'zona_total_mapas_merge13-geo.shp')
reservasgpd = gpd.read_file(reservasshp)

reservasgpd.head(1)

reservasgpd.shape

reservasgpd['centroide'] = reservasgpd['Ctrde']
reservasgpd['centroide'].head()

reservasoutgpd = reservasgpd.merge(df1, on='centroide')

reservasoutgpd.head(1)

"""### CBA"""

CBAnewINshp = os.path.join(data_folder, '50-CBAnew-IN.shp')
CBAnewINgpd = gpd.read_file(CBAnewINshp)

CBAnewINgpd.shape
CBAnewINgpd.head(1)

CBAnewINgpd['centroide'] = CBAnewINgpd['nom_ctdre']
CBAnewINgpd['centroide'].head(1)

CBAnewINgpd_out = CBAnewINgpd.merge(df1, on='centroide')

CBAnewINgpd_out.head(1)

"""### CORRIENTES"""

CORRIENTESINshp = os.path.join(data_folder, '50-CORRIENTES-IN.shp')
CORRIENTESINgpd = gpd.read_file(CORRIENTESINshp)
CORRIENTESINgpd.shape

CORRIENTESINgpd['centroide'] = CORRIENTESINgpd['CTRDE']

CORRIENTESINgpd_out = CORRIENTESINgpd.merge(df1, on='centroide')
CORRIENTESINgpd_out.head(1)

"""### CUENCA del SALADO"""

CuencaSaladoInshp = os.path.join(data_folder, 'P-CN_CuencaSalado.shp')
CuencaSaladoIngpd = gpd.read_file(CuencaSaladoInshp)
CuencaSaladoIngpd.shape

CuencaSaladoIngpd.head(1)

CuencaSaladoIngpd['centroide'] = CuencaSaladoIngpd['Centroide']

CuencaSaladoIngpd.drop('Centroide',
  axis='columns', inplace=True)
CuencaSaladoIngpd_out = CuencaSaladoIngpd.merge(df1, on='centroide')
CuencaSaladoIngpd_out.head(1)

"""### RESERVAS 500"""

R500_201709shp = os.path.join(data_folder, '500_201709.shp')
R500_201709shpIngpd = gpd.read_file(R500_201709shp)
R500_201709shpIngpd.shape

R500_201709shpIngpd.head(1)

R500_201709shpIngpd['centroide'] = R500_201709shpIngpd['Ctrde_ID']
#CBAnewINgpd['centroide'].head()
R500_201709shpIngpd_out = R500_201709shpIngpd.merge(df1, on='centroide')
R500_201709shpIngpd_out.head(1)

"""### GRABANDO SHP"""

output_file = 'RESERVAS.shp'
output_path = os.path.join(output_folder, output_file)
reservasoutgpd.to_file(output_path , mode="a")

output_file = 'RESERVAS_500.shp'
output_path = os.path.join(output_folder, output_file)
R500_201709shpIngpd_out.to_file(output_path , mode="a")

output_file = '50-CBAnew-OUT.shp'
output_path = os.path.join(output_folder, output_file)
CBAnewINgpd_out.to_file(output_path , mode="a")

output_file = 'P_CN_Cuenca_Salado.shp'
output_path = os.path.join(output_folder, output_file)
CuencaSaladoIngpd_out.to_file(output_path , mode="a")

output_file = '50-CORRIENTES-OUT.shp'
output_path = os.path.join(output_folder, output_file)
CORRIENTESINgpd_out.to_file(output_path , mode="a")