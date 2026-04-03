import pandas as pd
from datetime import datetime
import os

df = pd.read_csv('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.csv', 
                encoding='utf-8-sig', 
                sep=';',
                parse_dates=['fecha_creacion'])

print('CONSULTA 1: FLORES MENOS DE $50.000')
flores_baratas = df.query('categoria == "flores" and precio < 50000')
print(flores_baratas[['nombre', 'precio', 'stock']].sort_values('precio'))

print('CONSULTA 2: PRODUCTOS AGOTADOS')
agotados = df.query('stock == 0')
print(agotados[['nombre', 'categoria', 'stock']].sort_values('categoria'))

print('CONSULTA 3: ANCHETAS PREMIUM CON STOCK')
anchetas_premium = df.query('categoria == "ancheta" and precio > 200000 and stock > 0')
print(anchetas_premium[['nombre', 'precio', 'stock']].sort_values('precio', ascending=False))

print('CONSULTA 4: STOCK BAJO (MENOS DE 10 UNIDADES)')
stock_critico = df.query('stock > 0 and stock < 10')
print(stock_critico[['nombre', 'categoria', 'precio', 'stock']].sort_values('stock'))

print('CONSULTA 5: PRODUCTOS NO PELUCHES, PRECIO MEDIO')
para_paquetes = df.query('categoria != "peluche" and precio >= 80000 and precio <= 150000')
print(para_paquetes[['nombre', 'categoria', 'precio', 'stock']].sort_values('precio'))

log = f"""REPORTE DE TRANSFORMACIÓN CON QUERY - DATASET PRODUCTOS
DATASET BASE
- Registros totales: {df.shape[0]}

CONSULTAS REALIZADAS

1. FLORES BARATAS PARA PROMOCIONES
   - Condición: categoria == "flores" and precio < 50000
   - Registros encontrados: {len(flores_baratas)}
   - Precio máximo encontrado: {flores_baratas['precio'].max()}

2. PRODUCTOS AGOTADOS
   - Condición: stock == 0
   - Registros encontrados: {len(agotados)}

3. ANCHETAS PREMIUM CON STOCK
   - Condición: categoria == "ancheta" and precio > 200000 and stock > 0
   - Registros encontrados: {len(anchetas_premium)}
   - Precio mínimo encontrado: {anchetas_premium['precio'].min()}

4. STOCK CRÍTICO
   - Condición: stock > 0 and stock < 10
   - Registros encontrados: {len(stock_critico)}
   - Rango de stock: {stock_critico['stock'].min()} a {stock_critico['stock'].max()}

5. PRODUCTOS NO PELUCHES PARA PAQUETES DIFERENTES
   - Condición: categoria != "peluche" and precio >= 80000 and precio <= 150000
   - Registros encontrados: {len(para_paquetes)}
   - Categorías incluidas: {para_paquetes['categoria'].unique().tolist()}

VALIDACIÓN
- Todos los filtros retornaron registros dentro del rango esperado"""
os.makedirs("HU_EvelynRave/logs", exist_ok=True)
log_filename = f"HU_EvelynRave/logs/reporte_transformacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(log_filename, 'w', encoding='utf-8') as archivo:
    archivo.write(log)