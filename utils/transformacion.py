import pandas as pd
import os

def transformar_datos(data_frame_limpio):

    # -------------------------------------------------------
    # FILTRO 1 — ¿Cuántas anchetas se registraron por fecha?
    # Pregunta de negocio: ¿en qué fechas se agregan más anchetas?
    # Gráfica: líneas
    # -------------------------------------------------------
    filtro1 = data_frame_limpio.query("categoria == 'ancheta'")
    agrupacion1 = filtro1.groupby("fecha_creacion")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 2 — ¿Cuántos productos por categoría tienen precio >= 100.000?
    # Pregunta de negocio: ¿qué categoría tiene más productos premium?
    # Gráfica: barras
    # -------------------------------------------------------
    filtro2 = data_frame_limpio.query("precio >= 100000")
    agrupacion2 = filtro2.groupby("categoria")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 3 — ¿Qué combinación de categoría y nombre aparece más
    # en productos con precio >= 50.000?
    # Pregunta de negocio: ¿qué productos específicos dominan el catálogo medio-alto?
    # Gráfica: mapa de calor
    # -------------------------------------------------------
    filtro3 = data_frame_limpio.query("precio >= 50000")
    agrupacion3 = filtro3.groupby(["categoria", "nombre"])["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 4 — ¿Cuántos productos de cada categoría tienen stock <= 20?
    # Pregunta de negocio: ¿qué categorías están en riesgo de quedarse sin inventario?
    # Gráfica: barras (alerta de inventario)
    # -------------------------------------------------------
    filtro4 = data_frame_limpio.query("stock <= 20")
    agrupacion4 = filtro4.groupby("categoria")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # FILTRO 5 — ¿Cuántos productos de cada categoría tienen precio <= 50.000?
    # Pregunta de negocio: ¿qué categoría ofrece más opciones económicas?
    # Gráfica: torta
    # -------------------------------------------------------
    filtro5 = data_frame_limpio.query("precio <= 50000")
    agrupacion5 = filtro5.groupby("categoria")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # EXTRA — Distribución general por categoría (para KPIs y torta general)
    # -------------------------------------------------------
    agrupacion_general = data_frame_limpio.groupby("categoria")["id"].count().reset_index(name="conteo")

    # -------------------------------------------------------
    # EXPORTAR A JSON — React leerá estos archivos para los gráficos dinámicos
    # -------------------------------------------------------
    os.makedirs("BD_Analisis", exist_ok=True)
    agrupacion1.to_json("BD_Analisis/anchetas_por_fecha.json", orient="records", force_ascii=False, indent=2)
    agrupacion2.to_json("BD_Analisis/productos_premium_por_categoria.json", orient="records", force_ascii=False, indent=2)
    agrupacion3.to_json("BD_Analisis/calor_categoria_nombre.json", orient="records", force_ascii=False, indent=2)
    agrupacion4.to_json("BD_Analisis/stock_bajo_por_categoria.json", orient="records", force_ascii=False, indent=2)
    agrupacion5.to_json("BD_Analisis/productos_economicos_por_categoria.json", orient="records", force_ascii=False, indent=2)
    agrupacion_general.to_json("BD_Analisis/distribucion_general.json", orient="records", force_ascii=False, indent=2)

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