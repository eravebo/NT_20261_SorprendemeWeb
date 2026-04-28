import pandas as pd

def describir_datos(data_frame_limpio):
    print("*** DESCRIPCION DEL DATASET ***")
    print(f"Numero de filas: {data_frame_limpio.shape[0]}")
    print(f"Numero de columnas: {data_frame_limpio.shape[1]}")
    print(f"Lista de columnas: {list(data_frame_limpio.columns)}")
    print(f"Tipos de dato:\n{data_frame_limpio.dtypes}")

    # Estadisticas numericas
    print("*** ESTADISTICAS ***")
    print(data_frame_limpio[['id', 'precio', 'stock']].describe())

    # Conteos de columnas categoricas
    print("*** CONTEOS ***")
    print(data_frame_limpio['categoria'].value_counts())
    print(data_frame_limpio['nombre'].value_counts())

    # Fechas
    print("*** DESCRIPCION DE FECHAS ***")
    print(f"Fecha más antigua: {data_frame_limpio['fecha_creacion'].min()}")
    print(f"Fecha más reciente: {data_frame_limpio['fecha_creacion'].max()}")