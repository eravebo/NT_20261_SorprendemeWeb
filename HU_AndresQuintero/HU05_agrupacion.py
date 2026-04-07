import pandas as pd
from datetime import datetime
import os

# ============================================================
# HU 05 - Agrupación y resumen de datos tabla PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como analista de datos
# quiero agrupar información del dataset usando Pandas
# para obtener resúmenes e indicadores por categorías o segmentos.
# ============================================================

df = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.csv',
                encoding='utf-8-sig',
                sep=';',
                parse_dates=['fecha'])

print('AGRUPACIÓN 1: PEDIDOS POR ESTADO')
por_estado = df.groupby('estado').agg(
    total_pedidos=('id', 'count')
).reset_index().sort_values('total_pedidos', ascending=False)
print(por_estado)

print('AGRUPACIÓN 2: PEDIDOS POR AÑO Y ESTADO')
df['anio'] = df['fecha'].dt.year
por_anio_estado = df.groupby(['anio', 'estado']).agg(
    total_pedidos=('id', 'count')
).reset_index()
print(por_anio_estado)

print('AGRUPACIÓN 3: PEDIDOS POR MES EN 2024')
MESES = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
         7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
df['mes'] = df['fecha'].dt.month
df['mes_nombre'] = df['mes'].map(MESES)
por_mes_2024 = (df[df['anio'] == 2024]
                .groupby(['mes', 'mes_nombre'])
                .agg(total_pedidos=('id', 'count'))
                .reset_index()
                .sort_values('mes'))
print(por_mes_2024[['mes_nombre', 'total_pedidos']])

print('AGRUPACIÓN 4: PEDIDOS POR ESTADO DE MERCADOPAGO')
por_mp_status = df.groupby('mp_status').agg(
    total=('id', 'count')
).reset_index().sort_values('total', ascending=False)
print(por_mp_status)

log = f"""REPORTE DE AGRUPACIÓN CON GROUPBY - DATASET PEDIDOS
DATASET BASE
- Registros totales: {df.shape[0]}

AGRUPACIONES REALIZADAS

1. POR ESTADO
{por_estado.to_string(index=False)}

2. POR AÑO Y ESTADO
{por_anio_estado.to_string(index=False)}

3. POR MES EN 2024
{por_mes_2024[['mes_nombre', 'total_pedidos']].to_string(index=False)}

4. POR ESTADO DE MERCADOPAGO
{por_mp_status.to_string(index=False)}

RESUMEN EJECUTIVO
- Total pedidos: {df.shape[0]}
- Aprobados : {(df['estado'] == 'aprobado').sum()} ({round((df['estado'] == 'aprobado').sum()/df.shape[0]*100, 1)}%)
- Pendientes: {(df['estado'] == 'pendiente').sum()} ({round((df['estado'] == 'pendiente').sum()/df.shape[0]*100, 1)}%)
- Rechazados: {(df['estado'] == 'rechazado').sum()} ({round((df['estado'] == 'rechazado').sum()/df.shape[0]*100, 1)}%)
- Período: {df['fecha'].min().year} – {df['fecha'].max().year}"""

os.makedirs("HU_AndresQuintero/logs", exist_ok=True)
log_filename = f"HU_AndresQuintero/logs/reporte_agrupacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)
