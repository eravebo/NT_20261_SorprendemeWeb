import pandas as pd
import os
from datetime import datetime


def describir_datos_pedido(df):
    """
    HU 03 PEDIDO — Descripción exploratoria del dataset de pedidos de SorpréndemeWeb.
    Muestra head, tail, sample, info, describe y distribución por estado.
    Genera reporte .txt en logs/
    """
    print("*** DESCRIPCIÓN DEL DATASET PEDIDOS ***")
    print(f"Filas   : {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")
    print(f"Nombres : {df.columns.tolist()}")

    print("\nPRIMEROS 5 REGISTROS")
    print(df.head())

    print("\nÚLTIMOS 5 REGISTROS")
    print(df.tail())

    print("\n5 REGISTROS ALEATORIOS")
    print(df.sample(5))

    print("\nESTRUCTURA DEL DATASET")
    df.info()

    print("\nESTADÍSTICAS NUMÉRICAS")
    print(df.describe())

    numericas   = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categoricas = df.select_dtypes(include="object").columns.tolist()
    fechas      = df.select_dtypes(include="datetime64").columns.tolist()

    print(f"\nCOLUMNAS NUMÉRICAS  : {numericas}")
    print(f"COLUMNAS CATEGÓRICAS: {categoricas}")
    print(f"COLUMNAS FECHA      : {fechas}")

    print("\nDISTRIBUCIÓN POR ESTADO")
    print(df["estado"].value_counts())

    log = f"""REPORTE DE DESCRIPCIÓN - DATASET PEDIDOS

ESTRUCTURA
- Filas   : {df.shape[0]}
- Columnas: {df.shape[1]}
- Nombres : {df.columns.tolist()}

TIPOS DE DATOS
- Numéricas  : {numericas}
- Categóricas: {categoricas}
- Fechas     : {fechas}

ESTADÍSTICAS
- Rango de fechas: {df['fecha'].min()} a {df['fecha'].max()}

DISTRIBUCIÓN POR ESTADO
{df['estado'].value_counts().to_string()}

- Pedidos sin procesar por MercadoPago: {(df['mp_status'] == 'Sin procesar').sum()}"""

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/reporte_descripcion_pedido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(log)
