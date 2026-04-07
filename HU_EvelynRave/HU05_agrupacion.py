import pandas as pd
from datetime import datetime
import os

df = pd.read_csv('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.csv', 
                encoding='utf-8-sig', 
                sep=';',
                parse_dates=['fecha_creacion'])

print('AGRUPACIÓN 1: RESUMEN POR CATEGORÍA')
resumen_categoria = df.groupby('categoria').agg(
    total_productos = ('nombre', 'count'),
    precio_promedio = ('precio', 'mean'),
    precio_minimo   = ('precio', 'min'),
    precio_maximo   = ('precio', 'max'),
    stock_promedio  = ('stock', 'mean')
).round(0)

print(resumen_categoria)

print('AGRUPACIÓN 2: STOCK POR CATEGORÍA')
stock_categoria = df.groupby('categoria').agg(
    stock_total    = ('stock', 'sum'),
    stock_promedio = ('stock', 'mean'),
    agotados       = ('stock', lambda x: (x == 0).sum())
).round(0)

print(stock_categoria)

print('AGRUPACIÓN 3: EXTREMOS DE PRECIO POR CATEGORÍA')
for categoria in df['categoria'].unique():
    grupo = df[df['categoria'] == categoria]
    mas_caro = grupo.loc[grupo['precio'].idxmax(), 'nombre']
    mas_barato = grupo.loc[grupo['precio'].idxmin(), 'nombre']
    print(f'\n{categoria.upper()}')
    print(f'  Más caro:   {mas_caro} (${grupo["precio"].max():,})')
    print(f'  Más barato: {mas_barato} (${grupo["precio"].min():,})')
    if categoria == 'ancheta':
        ancheta_caro, ancheta_barato = mas_caro, mas_barato
    elif categoria == 'flores':
        flores_caro, flores_barato = mas_caro, mas_barato
    elif categoria == 'peluche':
        peluche_caro, peluche_barato = mas_caro, mas_barato

print('AGRUPACIÓN 4: PRODUCTOS POR RANGO DE PRECIO')

df['rango_precio'] = pd.cut(
    df['precio'],
    bins=[0, 50000, 150000, 250000, 400000],
    labels=['económico', 'medio', 'premium', 'lujo']
)

rango_categoria = df.groupby(['rango_precio', 'categoria'], observed=True).agg(
    total = ('nombre', 'count')
).reset_index()

print(rango_categoria)

print('AGRUPACIÓN 5: RESUMEN EJECUTIVO')
resumen_ejecutivo = df.groupby('categoria').agg(
    total_productos  = ('nombre', 'count'),
    precio_promedio  = ('precio', 'mean'),
    ingreso_potencial = ('precio', 'sum'),
    stock_total      = ('stock', 'sum'),
    productos_agotados = ('stock', lambda x: (x == 0).sum()),
    productos_criticos = ('stock', lambda x: ((x > 0) & (x < 10)).sum())
).round(0)

print(resumen_ejecutivo)

log = f"""REPORTE DE AGRUPACIONES - DATASET PRODUCTOS

DATASET BASE
- Registros totales: {df.shape[0]}
- Categorías analizadas: {df['categoria'].unique().tolist()}

AGRUPACIÓN 1: RESUMEN POR CATEGORÍA
{resumen_categoria.to_string()}

AGRUPACIÓN 2: STOCK POR CATEGORÍA
{stock_categoria.to_string()}

AGRUPACIÓN 3: EXTREMOS DE PRECIO
- ancheta:  más caro {ancheta_caro} | más barato {ancheta_barato}
- flores:   más caro {flores_caro} | más barato {flores_barato}
- peluche:  más caro {peluche_caro} | más barato {peluche_barato}

AGRUPACIÓN 4: DISTRIBUCIÓN POR RANGO DE PRECIO
{rango_categoria.to_string()}

AGRUPACIÓN 5: RESUMEN EJECUTIVO
{resumen_ejecutivo.to_string()}
"""

os.makedirs("HU_EvelynRave/logs", exist_ok=True)
log_filename = f"HU_EvelynRave/logs/reporte_agrupacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)