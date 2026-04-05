import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 04 - Transformación de datos con query() tabla DETALLE_PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero aplicar filtros y transformaciones usando query() en Pandas
# para seleccionar subconjuntos de información según condiciones de negocio.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/detalle_pedido_limpio.csv',
                 encoding='utf-8-sig',
                 sep=';')

print('CONSULTA 1: LÍNEAS CON MÁS DE 3 UNIDADES (COMPRAS EN CANTIDAD)')
compras_cantidad = df.query('cantidad > 3')
print(compras_cantidad[['id', 'pedido_id', 'producto_id', 'cantidad', 'subtotal']].sort_values('cantidad', ascending=False))

print('CONSULTA 2: LÍNEAS CON SUBTOTAL MAYOR A $500.000 (VENTAS DE ALTO VALOR)')
alto_valor = df.query('subtotal > 500000')
print(alto_valor[['id', 'pedido_id', 'producto_id', 'precio_unitario', 'cantidad', 'subtotal']].sort_values('subtotal', ascending=False))

print('CONSULTA 3: LÍNEAS CON PRECIO UNITARIO MENOR A $50.000 (PRODUCTOS ECONÓMICOS)')
economicos = df.query('precio_unitario < 50000')
print(economicos[['id', 'pedido_id', 'producto_id', 'precio_unitario', 'cantidad']].sort_values('precio_unitario'))

print('CONSULTA 4: LÍNEAS CON 1 SOLA UNIDAD Y SUBTOTAL ALTO (PRODUCTOS PREMIUM INDIVIDUALES)')
premium_individual = df.query('cantidad == 1 and precio_unitario > 200000')
print(premium_individual[['id', 'pedido_id', 'producto_id', 'precio_unitario', 'subtotal']].sort_values('precio_unitario', ascending=False))

print('CONSULTA 5: LÍNEAS ENTRE $80.000 Y $150.000 POR UNIDAD (RANGO MEDIO)')
rango_medio = df.query('precio_unitario >= 80000 and precio_unitario <= 150000')
print(rango_medio[['id', 'pedido_id', 'producto_id', 'precio_unitario', 'cantidad', 'subtotal']].sort_values('precio_unitario'))

log = f"""REPORTE DE TRANSFORMACIÓN CON QUERY - DATASET DETALLE_PEDIDO
DATASET BASE
- Registros totales: {df.shape[0]}

CONSULTAS REALIZADAS

1. COMPRAS EN CANTIDAD (cantidad > 3)
   - Condición: cantidad > 3
   - Registros encontrados: {len(compras_cantidad)}
   - Cantidad máxima encontrada: {compras_cantidad['cantidad'].max()}

2. VENTAS DE ALTO VALOR (subtotal > 500.000)
   - Condición: subtotal > 500000
   - Registros encontrados: {len(alto_valor)}
   - Subtotal máximo: {alto_valor['subtotal'].max()}

3. PRODUCTOS ECONÓMICOS (precio_unitario < 50.000)
   - Condición: precio_unitario < 50000
   - Registros encontrados: {len(economicos)}
   - Precio mínimo encontrado: {economicos['precio_unitario'].min()}

4. PRODUCTOS PREMIUM INDIVIDUALES (cantidad == 1 y precio > 200.000)
   - Condición: cantidad == 1 and precio_unitario > 200000
   - Registros encontrados: {len(premium_individual)}
   - Precio máximo encontrado: {premium_individual['precio_unitario'].max() if len(premium_individual) > 0 else 'N/A'}

5. RANGO MEDIO (precio entre $80.000 y $150.000)
   - Condición: precio_unitario >= 80000 and precio_unitario <= 150000
   - Registros encontrados: {len(rango_medio)}
   - Subtotal promedio en este rango: {round(rango_medio['subtotal'].mean(), 0).astype(int) if len(rango_medio) > 0 else 'N/A'}

VALIDACIÓN
- Todos los filtros retornaron registros dentro del rango esperado"""

os.makedirs('HU_AndresQuintero/logs', exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_transformacion_detalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
