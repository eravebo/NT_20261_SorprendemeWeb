import pandas as pd


def agrupar_datos_pedidos(df):
    """HU10 - Agrupacion y resumen de datos con groupby() - Tabla PEDIDO"""
    print("\n*** AGRUPACIONES CON groupby() - PEDIDO ***\n")

    # Agrupacion 1: Conteo y porcentaje de pedidos por estado
    # Permite ver cuantos pedidos hay en cada estado del ciclo de vida
    g1 = df.groupby("estado").agg(
        total_pedidos=("id", "count")
    ).reset_index()
    g1["porcentaje"] = (g1["total_pedidos"] / g1["total_pedidos"].sum() * 100).round(2)
    print("AGRUPACION 1 - Pedidos por estado:")
    print(g1.to_string(index=False))

    # Agrupacion 2: Pedidos por estado y presencia de MercadoPago
    # Permite cruzar el estado del pedido con si tiene pago registrado
    df_tmp = df.copy()
    df_tmp["tiene_mp"] = df_tmp["mp_payment_id"].notna().map({True: "Con MP", False: "Sin MP"})
    g2 = df_tmp.groupby(["estado", "tiene_mp"]).agg(
        total=("id", "count")
    ).reset_index()
    print("\nAGRUPACION 2 - Pedidos por estado y MercadoPago:")
    print(g2.to_string(index=False))

    # Agrupacion 3: Pedidos por mes y anio
    # Permite ver la actividad mensual de la tienda
    df_tmp2 = df.copy()
    df_tmp2["mes"] = df_tmp2["fecha"].dt.to_period("M").astype(str)
    g3 = df_tmp2.groupby("mes").agg(
        total_pedidos=("id", "count")
    ).reset_index().sort_values("mes")
    print("\nAGRUPACION 3 - Pedidos por mes:")
    print(g3.to_string(index=False))

    # Agrupacion 4: Estado de MercadoPago vs estado del pedido
    # Permite detectar inconsistencias entre el estado interno y el de la pasarela
    df_con_mp = df[df["mp_status"].notna()].copy()
    g4 = df_con_mp.groupby(["mp_status", "estado"]).agg(
        total=("id", "count")
    ).reset_index()
    print("\nAGRUPACION 4 - Estado MercadoPago vs estado pedido:")
    print(g4.to_string(index=False))

    return {"por_estado": g1, "estado_vs_mp": g2, "por_mes": g3, "mp_vs_estado": g4}


if __name__ == "__main__":
    from simulacion import generar_simulacion_pedidos
    from limpieza import limpiar_datos_pedidos
    simulaciones = generar_simulacion_pedidos(1000)
    df_sucio = pd.DataFrame(simulaciones)
    df_limpio = limpiar_datos_pedidos(df_sucio)
    agrupar_datos_pedidos(df_limpio)