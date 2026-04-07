import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 05 - Agrupación y resumen de datos tabla DETALLE_PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero agrupar información del dataset usando Pandas
# para obtener resúmenes e indicadores por categorías o segmentos.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/detalle_pedido_limpio.csv',
                 encoding='utf-8-sig',
                 sep=';')

print('AGRUPACIÓN 1: TOTAL DE UNIDADES Y VENTAS POR PRODUCTO')
por_producto = df.groupby('producto_id').agg(
    veces_pedido    = ('id',               'count'),
    unidades_totales= ('cantidad',         'sum'),
    ingreso_total   = ('subtotal',         'sum'),
    precio_promedio = ('precio_unitario',  'mean')
).reset_index()
por_producto['precio_promedio'] = por_producto['precio_promedio'].round(0).astype(int)
por_producto = por_producto.sort_values('ingreso_total', ascending=False)
print(por_producto.head(10))

print('AGRUPACIÓN 2: RESUMEN POR PEDIDO (CUÁNTOS PRODUCTOS Y CUÁNTO VALE CADA PEDIDO)')
por_pedido = df.groupby('pedido_id').agg(
    lineas_detalle  = ('id',       'count'),
    unidades_totales= ('cantidad', 'sum'),
    total_pedido    = ('subtotal', 'sum')
).reset_index()
por_pedido = por_pedido.sort_values('total_pedido', ascending=False)
print(por_pedido.head(10))

print('AGRUPACIÓN 3: DISTRIBUCIÓN DE CANTIDADES (¿CUÁNTAS LÍNEAS TIENEN 1, 2, 3... UNIDADES?)')
por_cantidad = df.groupby('cantidad').agg(
    total_lineas = ('id',       'count'),
    subtotal_sum = ('subtotal', 'sum')
).reset_index().sort_values('cantidad')
print(por_cantidad)

print('AGRUPACIÓN 4: SEGMENTACIÓN POR RANGO DE PRECIO UNITARIO')
bins   = [0, 50000, 100000, 200000, 350000]
labels = ['Económico (<50K)', 'Medio (50K-100K)', 'Alto (100K-200K)', 'Premium (>200K)']
df['rango_precio'] = pd.cut(df['precio_unitario'], bins=bins, labels=labels)

por_rango = df.groupby('rango_precio', observed=True).agg(
    total_lineas     = ('id',       'count'),
    unidades_totales = ('cantidad', 'sum'),
    ingreso_total    = ('subtotal', 'sum')
).reset_index()
print(por_rango)

log = f"""REPORTE DE AGRUPACIÓN CON GROUPBY - DATASET DETALLE_PEDIDO
DATASET BASE
- Registros totales: {df.shape[0]}

AGRUPACIONES REALIZADAS

1. POR PRODUCTO (top 5 por ingreso)
{por_producto.head(5).to_string(index=False)}

2. POR PEDIDO (top 5 por valor total)
{por_pedido.head(5).to_string(index=False)}

3. POR CANTIDAD
{por_cantidad.to_string(index=False)}

4. POR RANGO DE PRECIO UNITARIO
{por_rango.to_string(index=False)}

RESUMEN EJECUTIVO
- Total líneas de detalle : {df.shape[0]}
- Pedidos únicos          : {df['pedido_id'].nunique()}
- Productos únicos        : {df['producto_id'].nunique()}
- Unidades totales vendidas: {df['cantidad'].sum()}
- Ingresos totales        : ${df['subtotal'].sum():,}
- Ticket promedio por línea: ${int(df['subtotal'].mean()):,}"""

os.makedirs('HU_AndresQuintero/logs', exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_agrupacion_detalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
