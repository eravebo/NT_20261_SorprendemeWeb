import pandas as pd
import os

def limpiar_datos(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    # 1. Limpieza de textos
    data_frame_limpio['nombre'] = data_frame_limpio['nombre'].astype('string').str.strip().str.title()
    data_frame_limpio['categoria'] = data_frame_limpio['categoria'].astype('string').str.strip().str.lower()

    # 2. Validación de valores esperados
    valores_esperados_categoria = ['ancheta', 'flores', 'peluche']
    data_frame_limpio['categoria'] = data_frame_limpio['categoria'].where(
        data_frame_limpio['categoria'].isin(valores_esperados_categoria),
        pd.NA
    )

    # 3. Limpieza de numéricos
    data_frame_limpio['id'] = pd.to_numeric(data_frame_limpio['id'], errors='coerce')
    data_frame_limpio['precio'] = pd.to_numeric(data_frame_limpio['precio'], errors='coerce')
    data_frame_limpio['stock'] = pd.to_numeric(data_frame_limpio['stock'], errors='coerce')

    data_frame_limpio = data_frame_limpio[data_frame_limpio['id'] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio['precio'] > 0]

    # 4. Limpieza de fechas
    data_frame_limpio['fecha_creacion'] = pd.to_datetime(data_frame_limpio['fecha_creacion'], format='mixed', dayfirst=True)
    fecha_default = pd.to_datetime('2024-01-01')
    data_frame_limpio['fecha_creacion'] = data_frame_limpio['fecha_creacion'].fillna(fecha_default)

    # 5. Eliminar filas con campos obligatorios vacíos
    columnas_obligatorias = ['id', 'nombre', 'precio', 'categoria']
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)

    # 6. Exportar
    os.makedirs('BD_Limpieza', exist_ok=True)
    data_frame_limpio.to_csv('BD_Limpieza/productos_limpio.csv', index=False, encoding='utf-8-sig', sep=';')
    data_frame_limpio.to_json('BD_Limpieza/productos_limpio.json', orient='records', force_ascii=False, indent=2)

    print(f'Limpieza completada. Registros finales: {data_frame_limpio.shape[0]}')

    return data_frame_limpio