import os
import pandas as pd
from utils.graficacion import (
    graficar_lineas,
    graficar_barras,
    graficar_torta,
    graficar_mapa_calor,
    graficar_histograma
)

# Ruta compartida con los assets del frontend (misma que usa graficacion.py de Evelyn)
RUTA_ASSETS = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "assets", "graficos")


def graficar_pedidos_por_fecha(agrupacion1, ruta_destino=RUTA_ASSETS):
    # GRÁFICA 1 — Líneas
    # Muestra cuántos pedidos se registraron cada día.
    # Conclusión esperada: identificar las fechas con mayor volumen de pedidos.
    graficar_lineas(
        agrupacion1,
        columna_eje_x="fecha_dia",
        columna_eje_y="conteo",
        titulo="Pedidos registrados por fecha",
        color_linea="#E91E63",
        nombre_archivo="lineas_pedidos_por_fecha.png",
        ruta_destino=ruta_destino
    )


def graficar_pedidos_por_estado(agrupacion2, ruta_destino=RUTA_ASSETS):
    # GRÁFICA 2 — Barras
    # Compara la cantidad de pedidos en cada estado.
    # Conclusión esperada: ver qué estado predomina (pendiente, aprobado, rechazado).
    graficar_barras(
        agrupacion2,
        columna_categorias="estado",
        columna_valores="conteo",
        titulo="Cantidad de pedidos por estado",
        color_barras="#FF9800",
        nombre_archivo="barras_pedidos_por_estado.png",
        ruta_destino=ruta_destino
    )


def graficar_distribucion_mp_status(agrupacion5, ruta_destino=RUTA_ASSETS):
    # GRÁFICA 3 — Torta
    # Muestra la proporción de cada estado de pago MercadoPago.
    # Conclusión esperada: qué porcentaje de los pagos están aprobados, rechazados o pendientes.
    graficar_torta(
        agrupacion5,
        columna_etiquetas="mp_status",
        columna_valores="conteo",
        titulo="Distribución del estado de pago (MercadoPago)",
        lista_colores=["#4CAF50", "#F44336", "#FF9800", "#9E9E9E", "#2196F3"],
        nombre_archivo="torta_mp_status.png",
        ruta_destino=ruta_destino
    )


def graficar_estado_por_mes(agrupacion3, ruta_destino=RUTA_ASSETS):
    # GRÁFICA 4 — Mapa de calor
    # Cruza el mes con el estado del pedido y muestra la intensidad por volumen.
    # Conclusión esperada: identificar en qué meses se concentran los pedidos aprobados o rechazados.
    graficar_mapa_calor(
        agrupacion3,
        columna_filas="mes",
        columna_columnas="estado",
        columna_valores="conteo",
        titulo="Pedidos por mes y estado",
        paleta_color="YlOrRd",
        nombre_archivo="mapa_calor_pedidos_mes_estado.png",
        ruta_destino=ruta_destino
    )


def graficar_horas_pedido(data_frame_limpio, ruta_destino=RUTA_ASSETS):
    # GRÁFICA 5 — Histograma
    # Muestra en qué horas del día se realizan más pedidos.
    # Conclusión esperada: identificar los picos horarios de actividad de la tienda.
    df_con_hora = data_frame_limpio.copy()
    df_con_hora["hora"] = df_con_hora["fecha"].dt.hour

    graficar_histograma(
        df_con_hora,
        columna_valores="hora",
        titulo="Distribución de pedidos por hora del día",
        color_barras="#9C27B0",
        nombre_archivo="histograma_horas_pedido.png",
        ruta_destino=ruta_destino
    )
