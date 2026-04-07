import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 03 - Descripción exploratoria con Pandas tabla DETALLE_PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero usar Pandas para describir estadísticamente el set de datos
# para entender su estructura, distribución y calidad general.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/detalle_pedido_limpio.csv',
                 encoding='utf-8-sig',
                 sep=';')

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

print('COLUMNAS NUMÉRICAS')
numericas = df.select_dtypes(include=['int64', 'float64'])
print(numericas.columns.tolist())

print('COLUMNAS CATEGÓRICAS')
categoricas = df.select_dtypes(include='object')
# DETALLE_PEDIDO es tabla pivote: todas sus columnas son numéricas (IDs, cantidades, precios)
if categoricas.empty:
    print('Sin columnas categóricas — esta tabla es completamente numérica')
else:
    print(categoricas.columns.tolist())

log = f"""REPORTE DE DESCRIPCIÓN - DATASET DETALLE_PEDIDO

ESTRUCTURA
- Filas: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nombres: {df.columns.tolist()}

TIPOS DE DATOS
- Numéricas: {numericas.columns.tolist()}
- Categóricas: {categoricas.columns.tolist()}

ESTADÍSTICAS NUMÉRICAS
- Cantidad promedio por línea  : {df['cantidad'].mean().__round__(2)}
- Cantidad mínima              : {df['cantidad'].min()}
- Cantidad máxima              : {df['cantidad'].max()}
- Precio unitario promedio     : {df['precio_unitario'].mean().__round__(0).astype(int)}
- Precio unitario mínimo       : {df['precio_unitario'].min()}
- Precio unitario máximo       : {df['precio_unitario'].max()}
- Subtotal promedio por línea  : {df['subtotal'].mean().__round__(0).astype(int)}
- Subtotal total acumulado     : {df['subtotal'].sum()}

RELACIONES
- Pedidos únicos referenciados : {df['pedido_id'].nunique()}
- Productos únicos referenciados: {df['producto_id'].nunique()}
- Producto más pedido (id)     : {df['producto_id'].mode()[0]}"""

os.makedirs('HU_AndresQuintero/logs', exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_descripcion_detalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
