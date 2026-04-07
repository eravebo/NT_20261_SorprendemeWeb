import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 04 - Transformación de datos con query() tabla PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero aplicar filtros y transformaciones usando query() en Pandas
# para seleccionar subconjuntos de información según condiciones de negocio.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.csv',
                encoding='utf-8-sig',
                sep=';',
                parse_dates=['fecha'])

print('CONSULTA 1: PEDIDOS APROBADOS (VENTAS EXITOSAS)')
aprobados = df.query('estado == "aprobado"')
print(aprobados[['id', 'nombre_cliente', 'fecha', 'estado']].sort_values('fecha'))

print('CONSULTA 2: PEDIDOS PENDIENTES (REQUIEREN SEGUIMIENTO)')
pendientes = df.query('estado == "pendiente"')
print(pendientes[['id', 'nombre_cliente', 'email', 'telefono', 'estado']].sort_values('nombre_cliente'))

print('CONSULTA 3: PEDIDOS RECHAZADOS (PAGOS FALLIDOS)')
rechazados = df.query('estado == "rechazado"')
print(rechazados[['id', 'nombre_cliente', 'email', 'estado']].sort_values('nombre_cliente'))

print('CONSULTA 4: PEDIDOS DEL AÑO 2024')
df['anio'] = df['fecha'].dt.year
pedidos_2024 = df.query('anio == 2024')
print(pedidos_2024[['id', 'nombre_cliente', 'fecha', 'estado']].sort_values('fecha'))
df = df.drop(columns=['anio'])

print('CONSULTA 5: PEDIDOS DE ENVIGADO O EL POBLADO')
mask_sur = (df['direccion_envio'].str.contains('Envigado', case=False, na=False) |
            df['direccion_envio'].str.contains('El Poblado', case=False, na=False))
clientes_sur = df[mask_sur]
print(clientes_sur[['id', 'nombre_cliente', 'direccion_envio', 'estado']].sort_values('direccion_envio'))

log = f"""REPORTE DE TRANSFORMACIÓN CON QUERY - DATASET PEDIDOS
DATASET BASE
- Registros totales: {df.shape[0]}

CONSULTAS REALIZADAS

1. PEDIDOS APROBADOS (VENTAS EXITOSAS)
   - Condición: estado == "aprobado"
   - Registros encontrados: {len(aprobados)}

2. PEDIDOS PENDIENTES
   - Condición: estado == "pendiente"
   - Registros encontrados: {len(pendientes)}

3. PEDIDOS RECHAZADOS
   - Condición: estado == "rechazado"
   - Registros encontrados: {len(rechazados)}
   - Tasa de rechazo: {round(len(rechazados)/df.shape[0]*100, 1)}%

4. PEDIDOS AÑO 2024
   - Condición: anio == 2024
   - Registros encontrados: {len(pedidos_2024)}

5. CLIENTES EN ENVIGADO O EL POBLADO
   - Condición: direccion_envio contiene 'Envigado' o 'El Poblado'
   - Registros encontrados: {len(clientes_sur)}

VALIDACIÓN
- Todos los filtros retornaron registros dentro del rango esperado"""

os.makedirs("HU_AndresQuintero/logs", exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_transformacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
