import random
import pandas as pd
import os

# ============================================================
# HU 01 - Simulación y exportación de datos tabla DETALLE_PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como desarrollador de soluciones de datos
# quiero simular un conjunto de datos en Python y exportarlo en formatos CSV y JSON
# para disponer de información de prueba reutilizable en distintos escenarios.
# ============================================================

random.seed(42)

# --- Cargar IDs reales de PEDIDO y PRODUCTO para mantener coherencia entre tablas ---
df_pedidos   = pd.read_csv('HU_AndresQuintero/BD_LimpiezaDataSet/pedidos_limpio.csv',  encoding='utf-8-sig', sep=';')
df_productos = pd.read_csv('HU_EvelynRave/BD_LimpiezaDataSet/productos_limpio.csv', encoding='utf-8-sig', sep=';')

ids_pedidos   = df_pedidos['id'].tolist()
ids_productos = df_productos['id'].tolist()
precios_por_id = dict(zip(df_productos['id'], df_productos['precio']))

# --- Generar registros con IDs con posibles duplicados (dato sucio intencional) ---
registros = []
ids_generados = []
id_detalle = 1

for _ in range(1300):
    pedido_id   = random.choice(ids_pedidos)
    producto_id = random.choice(ids_productos)
    cantidad    = random.randint(1, 5)

    # precio_unitario: se toma del producto con pequeña variación (simulando cambios históricos de precio)
    precio_base = precios_por_id[producto_id]
    variacion   = random.uniform(0.90, 1.10)   # ±10%
    precio_unitario = round(precio_base * variacion, 2)

    # Introducir IDs duplicados intencionalmente (~15%) para que HU02 los limpie
    if ids_generados and random.random() < 0.15:
        nuevo_id = random.choice(ids_generados)
    else:
        nuevo_id = id_detalle
        id_detalle += 1
    ids_generados.append(nuevo_id)

    # Introducir algunos errores de formato en precio (~10%) para que HU02 los corrija
    if random.random() < 0.10:
        precio_unitario = str(precio_unitario).replace('.', ',')   # coma decimal (error de formato)

    registros.append({
        'id'              : nuevo_id,
        'pedido_id'       : pedido_id,
        'producto_id'     : producto_id,
        'cantidad'        : cantidad,
        'precio_unitario' : precio_unitario
    })

os.makedirs('HU_AndresQuintero/BD_Simulacion', exist_ok=True)
df = pd.DataFrame(registros)

ruta_csv  = 'HU_AndresQuintero/BD_Simulacion/detalle_pedido_dataset.csv'
ruta_json = 'HU_AndresQuintero/BD_Simulacion/detalle_pedido_dataset.json'

df.to_csv(ruta_csv,  index=False, encoding='utf-8-sig', sep=';')
df.to_json(ruta_json, orient='records', force_ascii=False, indent=2)

# --- Verificación ---
df_csv  = pd.read_csv(ruta_csv,  encoding='utf-8-sig', sep=';')
df_json = pd.read_json(ruta_json)

print(df.shape)
print(df_csv.shape)
print(df_json.shape)
