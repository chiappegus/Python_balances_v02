import pandas as pd
import numpy as np
import datetime as dt


### Cambiar nombre de archivo si corresponde
archivo = './archivo_balance/balances.txt'
sep = ','

# Cambiar segun la fecha del balance
fecha = dt.datetime(2025,1,28)

#¿Que prioridad se hace el mapa de maiz? --> depende de la campaña
prioridad_m11 = False
prioridad_m21 = False

# Que columnas deben quedar en el excel final
columnas_validas = ['centroide', 'P', 'S1', 'S2', 'TL', 'TC', 'M1', 'M2', 'A1', 'A2', 'G1', 'G2']

###############################################
#### CODIGO
###############################################
print('#### Se ordenan las columnas del archivo:', archivo)
print('#### para hacer los mapas de reserva')
print('#### Fecha del mapa de reserva:', fecha.strftime('%d-%m-%Y'))

print('Estas son las columnas que quedaran al final del script:')
print(columnas_validas)


if sep == ',':
    df1 = pd.read_csv(archivo, sep=',')
else:
    df1 = pd.read_csv(archivo, sep=';', header=0)

# Unimos las columnas de SOJA de primera y segunda
df1['S1'] = df1[['S1-III','S1-IV','S1-V','S1-VII']].sum(axis=1, numeric_only=True, min_count=1)
df1['S2'] = df1[['TS(S2)III','TS(S2)IV','TS(S2)V','TS(S2)VI']].sum(axis=1, numeric_only=True, min_count=1)

df1=df1.drop(columns={"S1-III","S1-IV","S1-V","S1-VII","TS(S2)III","TS(S2)IV","TS(S2)V","TS(S2)VI","CoordX","CoordY"})

# Renombramos las columnas de Girasol, Algodon y Trigo tardío
if sep == ';':
    df1.rename(columns={'A1,1': 'A1', 'A1,2': 'A2', 'G1,1': 'G1', 'G1,2': 'G2', 'TS(TC)':'TC'}, inplace=True)
else:
    df1.rename(columns={'A1.1': 'A1', 'A1.2': 'A2', 'G1.1': 'G1', 'G1.2': 'G2', 'TS(TC)':'TC'}, inplace=True)

# Unimos las columnas de Maiz de primera.
# Utilizamos el logical para definir cual tiene prioridad
if sep == ';':
    if prioridad_m11:
        print(u'Prioridad M11 en maíz de primera')
        df1['M1'] = df1['M1,1']
        # Completamos con los datos de M12
        df1.M1.fillna(df1['M1,2'], inplace=True)
    else:
        print(u'Prioridad M12 en maíz de primera')
        df1['M1'] = df1['M1,2']
        # Completamos con los datos de M11
        df1.M1.fillna(df1['M1,1'], inplace=True)
else:
    if prioridad_m11:
        print(u'Prioridad M11 en maíz de primera')
        df1['M1'] = df1['M1.1']
        # Completamos con los datos de M12
        df1.M1.fillna(df1['M1.2'], inplace=True)
    else:
        print(u'Prioridad M12 en maíz de primera')
        df1['M1'] = df1['M1.2']
        # Completamos con los datos de M11
        df1.M1.fillna(df1['M1.1'], inplace=True)

# Unimos las columnas de Maiz de segunda.
# Utilizamos el logical para definir cual tiene prioridad

if sep == ';':
    if prioridad_m21:
        print(u'Prioridad M21 en maíz de primera')
        df1['M2'] = df1['M2,1']
        # Completamos con los datos de M12
        df1.M2.fillna(df1['M2,2'], inplace=True)
    else:
        print(u'Prioridad M22 en maíz de primera')
        df1['M2'] = df1['M2,2']
        # Completamos con los datos de M11
        df1.M2.fillna(df1['M2,1'], inplace=True)
else:
    if prioridad_m21:
        print(u'Prioridad M21 en maíz de primera')
        df1['M2'] = df1['M2.1']
        # Completamos con los datos de M12
        df1.M2.fillna(df1['M2.2'], inplace=True)
    else:
        print(u'Prioridad M22 en maíz de primera')
        df1['M2'] = df1['M2.2']
        # Completamos con los datos de M11
        df1.M2.fillna(df1['M2.1'], inplace=True)

# Unimos las columnas de Trigo de primera TL y TS(TL)

df1['TL'] = df1[['TL','TS(TL)']].sum(axis=1, numeric_only=True, min_count=1)
df1.to_excel('test_antesdep.xlsx')

# Unimos las columnas de Pradera y Campo Natural
df1['P'] = df1[['P','CN']].sum(axis=1, numeric_only=True, min_count=1)

#################################
# Forma final del DataFrame
#################################
# Nos quedamos con las columnas que nos interesan
df = df1[columnas_validas]

# Agregamos la fila con No Agricola = -2000
nueva_fila = ['NA', -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000, -2000]
new = pd.DataFrame(columns=df.columns, data=[nueva_fila])
# Overwrite original dataframe
df = pd.concat([df, new], axis=0)
df = df.fillna(-1000)
# Usar 'centroide' como INDEX

df = df.set_index('centroide')
df = df.sort_index()

### Guardamos en excel
df.to_excel('Reservas_al_' + fecha.strftime('%Y%m%d') + '.xlsx')