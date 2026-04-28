import pandas as pd


def describir_datos_pedidos(df):
    print("\n*** DESCRIPCION DEL DATASET - PEDIDO ***")
    print(f"Numero de filas:    {df.shape[0]}")
    print(f"Numero de columnas: {df.shape[1]}")
    print(f"Lista de columnas:  {list(df.columns)}")

    print("\n*** TIPOS DE DATO ***")
    print(df.dtypes)

    print("\n*** MUESTRA - HEAD ***")
    print(df.head(5).to_string())

    print("\n*** MUESTRA - TAIL ***")
    print(df.tail(5).to_string())

    print("\n*** INFORMACION GENERAL (info) ***")
    df.info()

    print("\n*** ESTADISTICAS NUMERICAS ***")
    print(df[['id']].describe())

    print("\n*** CONTEOS - ESTADO ***")
    print(df['estado'].value_counts())

    print("\n*** CONTEOS - MP_STATUS ***")
    print(df['mp_status'].value_counts(dropna=False))

    print("\n*** PEDIDOS CON/SIN MERCADOPAGO ***")
    print(f"  Con MercadoPago: {df['mp_payment_id'].notna().sum()}")
    print(f"  Sin MercadoPago: {df['mp_payment_id'].isna().sum()}")

    print("\n*** DESCRIPCION DE FECHAS ***")
    print(f"  Fecha mas antigua:  {df['fecha'].min()}")
    print(f"  Fecha mas reciente: {df['fecha'].max()}")

    print("\n*** COLUMNAS CATEGORICAS VS NUMERICAS ***")
    print(f"  Categoricas: {df.select_dtypes(include=['object','string']).columns.tolist()}")
    print(f"  Numericas:   {df.select_dtypes(include='number').columns.tolist()}")


if __name__ == '__main__':
    from simulacion import generar_simulacion_pedidos
    from limpieza import limpiar_datos_pedidos
    simulaciones = generar_simulacion_pedidos(1000)
    df_sucio = pd.DataFrame(simulaciones)
    df_limpio = limpiar_datos_pedidos(df_sucio)
    describir_datos_pedidos(df_limpio)
    