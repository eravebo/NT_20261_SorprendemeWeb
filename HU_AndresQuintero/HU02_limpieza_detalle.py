import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 02 - Limpieza del set de datos tabla DETALLE_PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero limpiar un conjunto de datos con valores nulos, duplicados,
# errores de formato y datos inconsistentes
# para asegurar que la información sea confiable antes del análisis.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_Simulacion/detalle_pedido_dataset.csv', encoding='utf-8-sig', sep=';')
registros_originales = df.shape[0]
columnas_originales  = df.shape[1]

# --- CRITERIO 1: Valores nulos ---
nulos_por_columna = df.isnull().sum()
# Esta tabla no debería tener nulos (todas las columnas son obligatorias)
# Si los hay, los reportamos
total_nulos = nulos_por_columna.sum()

# --- CRITERIO 2: Duplicados por id ---
duplicados_eliminados = df['id'].duplicated().sum()
df = df.drop_duplicates(subset='id', keep='first')

# --- CRITERIO 3: Corregir tipos de datos ---
# precio_unitario puede tener comas decimales (error de formato introducido en HU01)
tipo_precio_antes  = df['precio_unitario'].dtype
ejemplo_precio_antes = df['precio_unitario'].iloc[0]

df['precio_unitario'] = (df['precio_unitario']
                         .astype(str)
                         .str.replace(',', '.', regex=False))
df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')

# Redondear a entero (igual que Evelyn hizo con precio en PRODUCTO)
df['precio_unitario'] = df['precio_unitario'].round(0).astype(int)

# Asegurar tipos correctos en las demás columnas
df['id']          = df['id'].astype(int)
df['pedido_id']   = df['pedido_id'].astype(int)
df['producto_id'] = df['producto_id'].astype(int)
df['cantidad']    = df['cantidad'].astype(int)

# --- CRITERIO 4: Normalización ---
# Validar que cantidad sea >= 1 (no puede haber 0 unidades en un detalle)
cantidad_invalida = (df['cantidad'] <= 0).sum()
df = df[df['cantidad'] > 0]

# Validar que precio_unitario sea > 0
precio_invalido = (df['precio_unitario'] <= 0).sum()
df = df[df['precio_unitario'] > 0]

# Agregar columna calculada: subtotal = cantidad * precio_unitario
df['subtotal'] = df['cantidad'] * df['precio_unitario']

log = f"""
REPORTE DE LIMPIEZA - DATASET DETALLE_PEDIDO

DATASET ORIGINAL
- Registros: {registros_originales}
- Columnas: {columnas_originales}

TRANSFORMACIONES REALIZADAS

1. NULOS
   - Total nulos encontrados: {total_nulos}
   - Detalle por columna: {nulos_por_columna.to_dict()}

2. DUPLICADOS
   - {duplicados_eliminados} registros eliminados
   - Criterio: se conservó la primera aparición por id

3. CORRECCIÓN DE TIPOS
   - Columna 'precio_unitario' tipo antes: {tipo_precio_antes}
   - Ejemplo antes: {ejemplo_precio_antes}
   - Tipo después: {df['precio_unitario'].dtype}
   - Comas decimales corregidas a punto decimal
   - Precio redondeado a entero

4. NORMALIZACIÓN
   - Registros con cantidad <= 0 eliminados: {cantidad_invalida}
   - Registros con precio <= 0 eliminados: {precio_invalido}
   - Columna 'subtotal' calculada (cantidad × precio_unitario)

DATASET FINAL
- Registros: {df.shape[0]}
- Columnas: {df.shape[1]}
- Nulos restantes: {df.isnull().sum().sum()}
"""

os.makedirs('HU_AndresQuintero/logs', exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_limpieza_detalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)

os.makedirs('HU_AndresQuintero/BD_LimpiezaDataSet', exist_ok=True)
df.to_csv('HU_AndresQuintero/BD_LimpiezaDataSet/detalle_pedido_limpio.csv',  index=False, encoding='utf-8-sig', sep=';')
df.to_json('HU_AndresQuintero/BD_LimpiezaDataSet/detalle_pedido_limpio.json', orient='records', force_ascii=False, indent=2)
