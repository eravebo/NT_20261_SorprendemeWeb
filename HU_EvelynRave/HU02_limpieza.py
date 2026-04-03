import pandas as pd
from datetime import datetime
import os

df = pd.read_csv('HU_EvelynRave/BD_Simulacion/productos_dataset.csv', encoding='utf-8-sig', sep=';')
registros_originales = df.shape[0]
columnas_originales = df.shape[1]

'''print('=== FORMA DEL DATASET ===')
print(df.shape)

print('=== TIPOS DE DATOS ===')
print(df.dtypes)

print('=== VALORES NULOS POR COLUMNA ===')
print(df.isnull().sum())

print('=== REGISTROS DUPLICADOS POR ID ===')
print(df['id'].duplicated().sum())

print('=== PRIMEROS 5 REGISTROS ===')
print(df.head())'''

#llenar valores nulos
nulos_descripcion = df['descripcion'].isnull().sum()
df['descripcion'] = df['descripcion'].fillna('Sin descripción disponible')

#trataiento de duplicados, decidimos mantener el primer registro encontradi y borrar los demas
duplicados_eliminados = df['id'].duplicated().sum()
df = df.drop_duplicates(subset='id', keep='first')


#normalizacion de datos en nombre y categoria

ejemplo_nombre_antes = df[['nombre']].iloc[10]
df['nombre'] = df['nombre'].str.title()
categorias_antes = df['categoria'].unique().tolist()
df['categoria'] = df['categoria'].str.lower()
df['precio'] = df['precio'].round(0).astype(int)


#unificación de formatos de fecha
tipo_fecha_antes = df['fecha_creacion'].dtype
ejemplo_fecha_antes = df['fecha_creacion'].iloc[0]
df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'], format='mixed', dayfirst=True)


log = f"""
REPORTE DE LIMPIEZA - DATASET PRODUCTOS

DATASET ORIGINAL
- Registros: {registros_originales}
- Columnas: {columnas_originales}

TRANSFORMACIONES REALIZADAS

1. NULOS
   - Columna 'descripcion': {nulos_descripcion} nulos rellenados con 'Sin descripción'

2. DUPLICADOS
   - {duplicados_eliminados} registros eliminados
   - Criterio: se conservó la primera aparición

3. NORMALIZACIÓN DE TEXTO
   - Columna 'nombre' antes: {ejemplo_nombre_antes}
   - Columna 'nombre' después: {df['nombre'].iloc[10]}
   - Categorías antes: {categorias_antes}
   - Categorías después: {df['categoria'].unique().tolist()}

4. FECHAS
   - Tipo antes: {tipo_fecha_antes}
   - Ejemplo antes: {ejemplo_fecha_antes}
   - Tipo después: {df['fecha_creacion'].dtype}
   - Ejemplo después: {df['fecha_creacion'].iloc[0]}

DATASET FINAL
- Registros: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nulos restantes: {df.isnull().sum().sum()}
"""
os.makedirs("HU_EvelynRave/logs", exist_ok=True)
log_filename = f"HU_EvelynRave/logs/reporte_limpieza_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)

os.makedirs("HU_EvelynRave/BD_LimpiezaDataSet", exist_ok=True)
df.to_csv('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.csv', index=False, encoding='utf-8-sig', sep=';')
df.to_json('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.json', orient='records', force_ascii=False, indent=2)
