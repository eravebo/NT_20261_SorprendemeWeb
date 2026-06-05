import pandas as pd

# IMPORTS — EVELYN RAVE (tabla PRODUCTO)
from utils.simulacion     import generar_simulacion
from utils.limpieza       import limpiar_datos
from utils.descripcion    import describir_datos
from utils.transformacion import transformar_datos
from utils.graficacion    import (
    graficar_lineas,
    graficar_barras,
    graficar_torta,
    graficar_mapa_calor,
    graficar_histograma
)

# ─────────────────────────────────────────────────────────────
# IMPORTS — ANDRÉS QUINTERO (tabla PEDIDO)
from utils.simulacion_pedido    import generar_simulacion_pedido
from utils.limpieza_pedido      import limpiar_datos_pedido
from utils.descripcion_pedido   import describir_datos_pedido
from utils.transformacion_pedido import transformar_datos_pedido
from utils.graficacion_pedido   import (
    graficar_pedidos_por_fecha,
    graficar_pedidos_por_estado,
    graficar_distribucion_mp_status,
    graficar_estado_por_mes,
    graficar_horas_pedido
)


# EVELYN RAVE — tabla PRODUCTO
print("\n" + "="*60)
print("  EVELYN RAVE — Tabla PRODUCTO")
print("="*60)

# ETAPA 1: Simulación (reemplazar por consumir_productos() cuando el back esté corriendo)
simulaciones     = generar_simulacion(1000)
data_frame_sucio = pd.DataFrame(simulaciones)

# ETAPA 2: Limpieza
data_frame_limpio = limpiar_datos(data_frame_sucio)

# ETAPA 3: Descripción
describir_datos(data_frame_limpio)

# ETAPA 4: Transformación y exportación de JSON
agrupaciones = transformar_datos(data_frame_limpio)

# ETAPA 5: Graficación — genera 5 gráficas como PNG en frontend/src/assets/graficos/

print("\n*** GRAFICACION ***")

# Gráfica 1 — Líneas: anchetas registradas por fecha
graficar_lineas(
    agrupaciones["agrupacion1"],
    columna_eje_x="fecha_creacion",
    columna_eje_y="conteo",
    titulo="Anchetas registradas por fecha",
    nombre_archivo="lineas_anchetas.png"
)

# Gráfica 2 — Barras: productos con precio mayor a $100.000 por categoría
graficar_barras(
    agrupaciones["agrupacion2"],
    columna_categorias="categoria",
    columna_valores="conteo",
    titulo="Productos premium (precio ≥ $100.000) por categoría",
    nombre_archivo="barras_premium.png"
)

# Gráfica 3 — Torta: distribución de productos económicos por categoría
graficar_torta(
    agrupaciones["agrupacion5"],
    columna_etiquetas="categoria",
    columna_valores="conteo",
    titulo="Productos económicos (precio ≤ $50.000) por categoría",
    nombre_archivo="torta_economicos.png"
)

# Gráfica 4 — Mapa de calor: categoría vs nombre en productos >= $50.000
graficar_mapa_calor(
    agrupaciones["agrupacion3"],
    columna_filas="categoria",
    columna_columnas="nombre",
    columna_valores="conteo",
    titulo="Categoría vs Nombre — productos con precio ≥ $50.000",
    nombre_archivo="mapa_calor_categoria_nombre.png"
)

# Gráfica 5 — Histograma: distribución de precios de todos los productos
graficar_histograma(
    data_frame_limpio,
    columna_valores="precio",
    titulo="Distribución de precios de productos",
    nombre_archivo="histograma_precios.png"
)

print("\n✅ Pipeline de productos completado.")
print("   PNG → frontend/src/assets/graficos/")
print("   JSON → BD_Analisis/")


# =============================================================
# ANDRÉS QUINTERO — tabla PEDIDO
# =============================================================
print("\n" + "="*60)
print("  ANDRÉS QUINTERO — Tabla PEDIDO")
print("="*60)

# ETAPA 1: Simulación (reemplazar por consumir_pedidos() cuando el back esté corriendo)
df_pedidos_crudo  = generar_simulacion_pedido(1300)

# ETAPA 2: Limpieza
df_pedidos_limpio = limpiar_datos_pedido(df_pedidos_crudo)

# ETAPA 3: Descripción
describir_datos_pedido(df_pedidos_limpio)

# ETAPA 4: Transformación y exportación de JSON
agrupaciones_pedido = transformar_datos_pedido(df_pedidos_limpio)

# ETAPA 5: Graficación — genera 5 gráficas como PNG en frontend/src/assets/graficos/

print("\n*** GRAFICACION ***")

# Gráfica 1 — Líneas: pedidos registrados por fecha
graficar_pedidos_por_fecha(agrupaciones_pedido["agrupacion1"])

# Gráfica 2 — Barras: cantidad de pedidos por estado
graficar_pedidos_por_estado(agrupaciones_pedido["agrupacion2"])

# Gráfica 3 — Torta: distribución del estado de pago MercadoPago
graficar_distribucion_mp_status(agrupaciones_pedido["agrupacion5"])

# Gráfica 4 — Mapa de calor: pedidos por mes y estado
graficar_estado_por_mes(agrupaciones_pedido["agrupacion3"])

# Gráfica 5 — Histograma: distribución de pedidos por hora del día
graficar_horas_pedido(df_pedidos_limpio)

print("\n✅ Pipeline de pedidos completado.")
print("   PNG → frontend/src/assets/graficos/")
print("   JSON → BD_Analisis/")