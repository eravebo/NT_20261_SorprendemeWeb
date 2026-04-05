import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 03 - Descripción exploratoria con Pandas tabla PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero usar Pandas para describir estadísticamente el set de datos
# para entender su estructura, distribución y calidad general.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.csv',
                encoding='utf-8-sig',
                sep=';',
                parse_dates=['fecha'])

# --- Forma del dataset ---
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

log = f"""REPORTE DE DESCRIPCIÓN - DATASET PEDIDOS

ESTRUCTURA
- Filas: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nombres: {df.columns.tolist()}

TIPOS DE DATOS
- Numéricas: {numericas.columns.tolist()}
- Categóricas: {categoricas.columns.tolist()}
- Fechas: {fechas.columns.tolist()}

ESTADÍSTICAS NUMÉRICAS
- Total pedidos: {df.shape[0]}
- Rango de fechas: {df['fecha'].min()} a {df['fecha'].max()}

ESTADÍSTICAS CATEGÓRICAS
- Estados únicos: {df['estado'].nunique()}
- Estado más frecuente: {df['estado'].mode()[0]}
- Pedidos sin procesar por MercadoPago: {(df['mp_status'] == 'Sin procesar').sum()}

DISTRIBUCIÓN POR ESTADO
- Aprobados : {(df['estado'] == 'aprobado').sum()}
- Pendientes: {(df['estado'] == 'pendiente').sum()}
- Rechazados: {(df['estado'] == 'rechazado').sum()}"""

os.makedirs("HU_AndresQuintero/logs", exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_descripcion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
