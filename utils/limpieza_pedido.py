import pandas as pd
import os
from datetime import datetime


def limpiar_datos_pedido(df):
    """
    HU 02 PEDIDO — Limpia el dataset de pedidos de SorpréndemeWeb.
    - Rellena nulos en mp_payment_id y mp_status con 'Sin procesar'
    - Elimina duplicados por id (conserva primera aparición)
    - Unifica fechas en 4 formatos distintos a datetime
    - Normaliza 'estado' y 'email' a minúsculas sin espacios
    - Genera reporte .txt en logs/
    - Exporta pedidos_limpio.csv y .json a BD_Limpieza/
    """
    df_limpio = df.copy()
    registros_originales = df_limpio.shape[0]

    # 1. Nulos
    nulos_mp_payment = df_limpio["mp_payment_id"].isnull().sum()
    nulos_mp_status  = df_limpio["mp_status"].isnull().sum()
    df_limpio["mp_payment_id"] = df_limpio["mp_payment_id"].fillna("Sin procesar")
    df_limpio["mp_status"]     = df_limpio["mp_status"].fillna("Sin procesar")

    # 2. Duplicados
    duplicados_eliminados = df_limpio["id"].duplicated().sum()
    df_limpio = df_limpio.drop_duplicates(subset="id", keep="first")

    # 3. Normalización de texto
    df_limpio["estado"]          = df_limpio["estado"].astype(str).str.lower().str.strip()
    df_limpio["email"]           = df_limpio["email"].astype(str).str.lower().str.strip()
    df_limpio["nombre_cliente"]  = df_limpio["nombre_cliente"].astype(str).str.strip()

    # 4. Fechas
    tipo_fecha_antes    = df_limpio["fecha"].dtype
    ejemplo_fecha_antes = df_limpio["fecha"].iloc[0]
    df_limpio["fecha"]  = pd.to_datetime(df_limpio["fecha"], format="mixed", dayfirst=True)

    # 5. Validar estados permitidos
    estados_encontrados = set(df_limpio["estado"].unique())

    log = f"""
REPORTE DE LIMPIEZA - DATASET PEDIDOS

DATASET ORIGINAL
- Registros: {registros_originales}
- Columnas : {df.shape[1]}

TRANSFORMACIONES REALIZADAS

1. NULOS
   - Columna 'mp_payment_id': {nulos_mp_payment} nulos rellenados con 'Sin procesar'
   - Columna 'mp_status'    : {nulos_mp_status} nulos rellenados con 'Sin procesar'

2. DUPLICADOS
   - {duplicados_eliminados} registros eliminados
   - Criterio: se conservó la primera aparición por id

3. NORMALIZACIÓN DE TEXTO
   - Columna 'estado' normalizada a minúsculas
   - Columna 'email' normalizada a minúsculas
   - Estados válidos encontrados: {estados_encontrados}

4. FECHAS
   - Tipo antes   : {tipo_fecha_antes}
   - Ejemplo antes: {ejemplo_fecha_antes}
   - Tipo después : {df_limpio["fecha"].dtype}
   - Ejemplo después: {df_limpio["fecha"].iloc[0]}

DATASET FINAL
- Registros     : {df_limpio.shape[0]}
- Columnas      : {df_limpio.shape[1]}
- Nulos restantes: {df_limpio.isnull().sum().sum()}
"""
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/reporte_limpieza_pedido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(log)

    os.makedirs("BD_Limpieza", exist_ok=True)
    df_limpio.to_csv("BD_Limpieza/pedidos_limpio.csv",  index=False, encoding="utf-8-sig", sep=";")
    df_limpio.to_json("BD_Limpieza/pedidos_limpio.json", orient="records", force_ascii=False, indent=2)

    print(f"Limpieza PEDIDO completada. Registros finales: {df_limpio.shape[0]}")
    return df_limpio
