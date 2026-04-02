import pandas as pd
from datetime import datetime
import os

df = pd.read_csv('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.csv', 
                encoding='utf-8-sig', 
                sep=';',
                parse_dates=['fecha_creacion'])

#forma del dataset
print(f'Filas: {df.shape[0]}')
print(f'Columnas: {df.shape[1]}')
print(f'Nombres de columnas: {df.columns.tolist()}')

print('PRIMEROS 5 REGISTROS')
print(df.head())

print('ÚLTIMOS 5 REGISTROS')
print(df.tail())

print('5 REGISTROS ALEATORIOS')
print(df.sample(5))

print('ESTRUCTURA DEL DATASET')
df.info()

print('ESTADÍSTICAS COLUMNAS NUMÉRICAS')
print(df.describe())

print('ESTADÍSTICAS COLUMNAS DE TEXTO')
print(df.describe(include='object'))

print('COLUMNAS NUMÉRICAS')
numericas = df.select_dtypes(include=['int64', 'float64'])
print(numericas.columns.tolist())

print('COLUMNAS CATEGÓRICAS')
categoricas = df.select_dtypes(include='object')
print(categoricas.columns.tolist())

print('COLUMNAS DE FECHA')
fechas = df.select_dtypes(include='datetime64')
print(fechas.columns.tolist())

log = f"""REPORTE DE DESCRIPCIÓN - DATASET PRODUCTOS

ESTRUCTURA
- Filas: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nombres: {df.columns.tolist()}

TIPOS DE DATOS
- Numéricas: {numericas.columns.tolist()}
- Categóricas: {categoricas.columns.tolist()}
- Fechas: {fechas.columns.tolist()}

ESTADÍSTICAS NUMÉRICAS
- Precio promedio: {round(df['precio'].mean(), 2)}
- Stock mínimo: {df['stock'].min()}
- Stock máximo: {df['stock'].max()}
- Rango de fechas: {df['fecha_creacion'].min()} a {df['fecha_creacion'].max()}

ESTADÍSTICAS CATEGÓRICAS
- Categorías únicas: {df['categoria'].nunique()}
- Nombre más frecuente: {df['nombre'].mode()[0]}
- Registros sin descripción original: {(df['descripcion'] == 'Sin descripción disponible').sum()}"""

os.makedirs("HU_EvelynRave/logs", exist_ok=True)
log_filename = f"HU_EvelynRave/logs/reporte_descripcion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)