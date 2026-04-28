import pandas as pd
import os


def limpiar_datos_pedidos(data_frame_sucio):
    df = data_frame_sucio.copy()

    # 1. Limpieza de IDs
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df = df[df['id'] > 0]

    # 2. Nombre del cliente: strip y title
    df['nombre_cliente'] = df['nombre_cliente'].astype('string').str.strip().str.title()

    # 3. Telefono: eliminar prefijos de texto, solo dejar digitos
    df['telefono'] = df['telefono'].astype('string').str.replace(r'[^0-9]', '', regex=True).str.strip()
    df['telefono'] = df['telefono'].where(df['telefono'].str.len() >= 7, pd.NA)

    # 4. Email: validar formato con regex
    patron_email = r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$'
    df['email'] = df['email'].astype('string')
    df['email'] = df['email'].where(df['email'].str.match(patron_email, na=False), pd.NA)

    # 5. Direccion: strip de espacios
    df['direccion_envio'] = df['direccion_envio'].astype('string').str.strip()

    # 6. Fechas: multiples formatos -> datetime
    df['fecha'] = pd.to_datetime(df['fecha'], format='mixed', dayfirst=True, errors='coerce')
    df['fecha'] = df['fecha'].fillna(pd.to_datetime('2024-01-01'))

    # 7. Estado: minusculas y validar valores permitidos
    valores_validos = ['pendiente', 'aprobado', 'rechazado']
    df['estado'] = df['estado'].astype('string').str.strip().str.lower()
    df['estado'] = df['estado'].where(df['estado'].isin(valores_validos), pd.NA)

    # 8. Campos NULLABLE: mp_payment_id y mp_status se dejan tal cual
    df['mp_payment_id'] = df['mp_payment_id'].astype('string').where(df['mp_payment_id'].notna(), pd.NA)
    df['mp_status'] = df['mp_status'].astype('string').where(df['mp_status'].notna(), pd.NA)

    # 9. Eliminar filas con campos obligatorios vacios
    columnas_obligatorias = ['id', 'nombre_cliente', 'telefono', 'email', 'direccion_envio', 'fecha', 'estado']
    df = df.dropna(subset=columnas_obligatorias)

    # 10. Exportar
    os.makedirs('BD_Limpieza', exist_ok=True)
    df.to_csv('BD_Limpieza/pedidos_limpio.csv', index=False, encoding='utf-8-sig', sep=';')
    df.to_json('BD_Limpieza/pedidos_limpio.json', orient='records', force_ascii=False, indent=2)

    print(f'Limpieza completada. Registros finales: {df.shape[0]}')
    return df


if __name__ == '__main__':
    from simulacion import generar_simulacion_pedidos
    simulaciones = generar_simulacion_pedidos(1000)
    df_sucio = pd.DataFrame(simulaciones)
    df_limpio = limpiar_datos_pedidos(df_sucio)
    print(df_limpio.head(10).to_string())