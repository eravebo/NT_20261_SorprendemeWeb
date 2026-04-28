import pandas as pd


def aplicar_queries_pedidos(df):
    """HU09 - Transformacion con query() de Pandas - Tabla PEDIDO"""
    print("\n*** CONSULTAS CON query() - PEDIDO ***\n")

    # Consulta 1: Pedidos aprobados
    # Necesidad: ver todas las ordenes que completaron el pago
    q1 = df[df["estado"] == "aprobado"]
    print(f"CONSULTA 1 - Pedidos aprobados: {q1.shape[0]} registros")
    print(q1[["id", "nombre_cliente", "email", "estado", "fecha"]].head(5).to_string(index=False))

    # Consulta 2: Pedidos pendientes sin pago en MercadoPago
    # Necesidad: identificar pedidos que nunca iniciaron pago
    q2 = df[(df["estado"] == "pendiente") & (df["mp_payment_id"].isna())]
    print(f"\nCONSULTA 2 - Pendientes sin MercadoPago: {q2.shape[0]} registros")
    print(q2[["id", "nombre_cliente", "estado", "mp_payment_id", "fecha"]].head(5).to_string(index=False))

    # Consulta 3: Pedidos rechazados con pago registrado
    # Necesidad: detectar transacciones fallidas en la pasarela
    q3 = df[(df["estado"] == "rechazado") & (df["mp_payment_id"].notna())]
    print(f"\nCONSULTA 3 - Rechazados CON MercadoPago: {q3.shape[0]} registros")
    print(q3[["id", "nombre_cliente", "estado", "mp_payment_id", "mp_status"]].head(5).to_string(index=False))

    # Consulta 4: Pedidos del anio 2025
    # Necesidad: filtrar actividad anual para reportes de gestion
    df_tmp = df.copy()
    df_tmp["anio"] = df_tmp["fecha"].dt.year
    q4 = df_tmp[df_tmp["anio"] == 2025]
    print(f"\nCONSULTA 4 - Pedidos del 2025: {q4.shape[0]} registros")
    print(q4[["id", "nombre_cliente", "fecha", "estado"]].head(5).to_string(index=False))

    return {"aprobados": q1, "pendientes_sin_pago": q2, "rechazados_con_mp": q3, "pedidos_2025": q4}


if __name__ == "__main__":
    from simulacion import generar_simulacion_pedidos
    from limpieza import limpiar_datos_pedidos
    simulaciones = generar_simulacion_pedidos(1000)
    df_sucio = pd.DataFrame(simulaciones)
    df_limpio = limpiar_datos_pedidos(df_sucio)
    aplicar_queries_pedidos(df_limpio)