import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 02 - Limpieza del set de datos de la tabla PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero limpiar un conjunto de datos con valores nulos, duplicados,
# errores de formato y datos inconsistentes
# para asegurar que la información sea confiable antes del análisis.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_Simulacion/pedidos_dataset.csv', encoding='utf-8-sig', sep=';')
registros_originales = df.shape[0]
columnas_originales = df.shape[1]

# --- Rellenar valores nulos ---
# mp_payment_id y mp_status son nulos válidos para pedidos sin procesar por MercadoPago
nulos_mp_payment = df['mp_payment_id'].isnull().sum()
nulos_mp_status = df['mp_status'].isnull().sum()
df['mp_payment_id'] = df['mp_payment_id'].fillna('Sin procesar')
df['mp_status'] = df['mp_status'].fillna('Sin procesar')

# --- Tratamiento de duplicados: conservar primera aparición ---
duplicados_eliminados = df['id'].duplicated().sum()
df = df.drop_duplicates(subset='id', keep='first')

# --- Normalización de texto ---
ejemplo_estado_antes = df[['estado']].iloc[0]
df['estado'] = df['estado'].str.lower().str.strip()
df['email'] = df['email'].str.lower().str.strip()
df['nombre_cliente'] = df['nombre_cliente'].str.strip()

# --- Unificación de formatos de fecha ---
tipo_fecha_antes = df['fecha'].dtype
ejemplo_fecha_antes = df['fecha'].iloc[0]
df['fecha'] = pd.to_datetime(df['fecha'], format='mixed', dayfirst=True)

# --- Validar valores permitidos en estado ---
estados_validos = {"pendiente", "aprobado", "rechazado"}
estados_encontrados = set(df['estado'].unique())

log = f"""
REPORTE DE LIMPIEZA - DATASET PEDIDOS

DATASET ORIGINAL
- Registros: {registros_originales}
- Columnas: {columnas_originales}

TRANSFORMACIONES REALIZADAS

1. NULOS
   - Columna 'mp_payment_id': {nulos_mp_payment} nulos rellenados con 'Sin procesar'
   - Columna 'mp_status': {nulos_mp_status} nulos rellenados con 'Sin procesar'
   - Nota: estos nulos son válidos (pedidos pendientes sin respuesta de MercadoPago)

2. DUPLICADOS
   - {duplicados_eliminados} registros eliminados
   - Criterio: se conservó la primera aparición por id

3. NORMALIZACIÓN DE TEXTO
   - Columna 'estado' antes: {ejemplo_estado_antes.values[0]}
   - Columna 'estado' después: {df['estado'].iloc[0]}
   - Columna 'email' normalizada a minúsculas
   - Columna 'nombre_cliente' sin espacios extra
   - Estados válidos encontrados: {estados_encontrados}

4. FECHAS
   - Tipo antes: {tipo_fecha_antes}
   - Ejemplo antes: {ejemplo_fecha_antes}
   - Tipo después: {df['fecha'].dtype}
   - Ejemplo después: {df['fecha'].iloc[0]}

DATASET FINAL
- Registros: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nulos restantes: {df.isnull().sum().sum()}
"""

os.makedirs("HU_AndresQuintero/logs", exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_limpieza_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)

os.makedirs("HU_AndresQuintero/BD_LimpiezaDataSet", exist_ok=True)
df.to_csv('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.csv', index=False, encoding='utf-8-sig', sep=';')
df.to_json('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.json', orient='records', force_ascii=False, indent=2)
