import pandas as pd
import os

def transformar_datos_pedido(data_frame_limpio):

    df = data_frame_limpio.copy()
    df["fecha_dia"] = df["fecha"].dt.date.astype(str)
    df["mes"]       = df["fecha"].dt.to_period("M").astype(str)

    # -------------------------------------------------------
    # FILTRO 1 — ¿Cuántos pedidos se registraron por fecha?
    # Pregunta de negocio: ¿en qué fechas hay mayor actividad de pedidos?
    # Gráfica: líneas
    # -------------------------------------------------------
    agrupacion1 = df.groupby("fecha_dia")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 2 — ¿Cuántos pedidos hay por estado?
    # Pregunta de negocio: ¿cuántos pedidos están pendientes, aprobados o rechazados?
    # Gráfica: barras
    # -------------------------------------------------------
    agrupacion2 = df.groupby("estado")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 3 — ¿Cómo se distribuye la cantidad de pedidos por estado y mes?
    # Pregunta de negocio: ¿cómo varía el flujo de pedidos en el tiempo según su estado?
    # Gráfica: mapa de calor
    # -------------------------------------------------------
    agrupacion3 = df.groupby(["mes", "estado"])["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 4 — ¿Cuántos pedidos aprobados se registraron por mes?
    # Pregunta de negocio: ¿cuál es la tendencia de pedidos exitosos mes a mes?
    # Gráfica: barras
    # -------------------------------------------------------
    filtro4     = df.query("estado == 'aprobado'")
    agrupacion4 = filtro4.groupby("mes")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 5 — ¿Cómo se distribuye el estado de pago MercadoPago?
    # Pregunta de negocio: ¿qué proporción de los pagos están aprobados, rechazados o pendientes?
    # Gráfica: torta
    # -------------------------------------------------------
    agrupacion5 = df.groupby("mp_status")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # EXTRA — Distribución general por estado (para KPIs y torta general)
    # -------------------------------------------------------
    agrupacion_general = df.groupby("estado")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # EXPORTAR A JSON — React leerá estos archivos para los gráficos dinámicos
    # -------------------------------------------------------
    os.makedirs("BD_Analisis", exist_ok=True)
    agrupacion1.to_json("BD_Analisis/pedidos_por_fecha.json",                 orient="records", force_ascii=False, indent=2)
    agrupacion2.to_json("BD_Analisis/pedidos_por_estado.json",                orient="records", force_ascii=False, indent=2)
    agrupacion3.to_json("BD_Analisis/pedidos_estado_por_mes.json",            orient="records", force_ascii=False, indent=2)
    agrupacion4.to_json("BD_Analisis/pedidos_aprobados_por_mes.json",         orient="records", force_ascii=False, indent=2)
    agrupacion5.to_json("BD_Analisis/distribucion_mp_status.json",            orient="records", force_ascii=False, indent=2)
    agrupacion_general.to_json("BD_Analisis/distribucion_pedidos_general.json", orient="records", force_ascii=False, indent=2)

    print("Archivos JSON exportados en BD_Analisis/")

    agrupacion_resumen = {
        "agrupacion1": agrupacion1,
        "agrupacion2": agrupacion2,
        "agrupacion3": agrupacion3,
        "agrupacion4": agrupacion4,
        "agrupacion5": agrupacion5,
        "agrupacion_general": agrupacion_general
    }

    return agrupacion_resumen
