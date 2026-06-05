import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ruta donde se guardan las imágenes para que React las pueda mostrar.
# utils/ está un nivel abajo de la raíz, por eso se sube con ".."
RUTA_ASSETS = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "assets", "graficos")


def crear_ruta_si_no_existe(ruta_destino):
    os.makedirs(ruta_destino, exist_ok=True)


def graficar_lineas(datos_agrupados, columna_eje_x, columna_eje_y,
                    titulo="Gráfico de líneas", color_linea="#2196F3",
                    nombre_archivo="lineas.png", ruta_destino=RUTA_ASSETS):
    # GRÁFICA 1 — Líneas
    # Muestra tendencias a lo largo del tiempo.
    # Conclusión esperada: identificar en qué fechas se registran más anchetas.

    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    area_dibujo.plot(
        datos_agrupados[columna_eje_x],
        datos_agrupados[columna_eje_y],
        marker="o", color=color_linea, linewidth=2
    )

    area_dibujo.set_title(titulo, fontsize=14)
    area_dibujo.set_xlabel(columna_eje_x, fontsize=12)
    area_dibujo.set_ylabel(columna_eje_y, fontsize=12)
    area_dibujo.grid(True, linestyle="--", alpha=0.6)

    n = len(datos_agrupados[columna_eje_x])
    if n > 20:
        step = max(1, n // 12)
        indices = list(range(0, n, step))
        area_dibujo.set_xticks(indices)
        area_dibujo.set_xticklabels(
            [datos_agrupados[columna_eje_x].iloc[i] for i in indices],
            rotation=45, ha="right"
        )
    else:
        plt.xticks(rotation=45)

    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print(f"Gráfico de líneas guardado en: {ruta_completa}")


def graficar_barras(datos_agrupados, columna_categorias, columna_valores,
                    titulo="Gráfico de barras", color_barras="#4CAF50",
                    nombre_archivo="barras.png", ruta_destino=RUTA_ASSETS):
    # GRÁFICA 2 — Barras
    # Compara cantidades entre categorías.
    # Conclusión esperada: ver qué categoría tiene más productos premium.

    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    area_dibujo.bar(
        datos_agrupados[columna_categorias],
        datos_agrupados[columna_valores],
        color=color_barras, edgecolor="black"
    )

    area_dibujo.set_title(titulo, fontsize=14)
    area_dibujo.set_xlabel(columna_categorias, fontsize=12)
    area_dibujo.set_ylabel(columna_valores, fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print(f"Gráfico de barras guardado en: {ruta_completa}")


def graficar_torta(datos_agrupados, columna_etiquetas, columna_valores,
                   titulo="Gráfico de torta", lista_colores=None,
                   nombre_archivo="torta.png", ruta_destino=RUTA_ASSETS):
    # GRÁFICA 3 — Torta
    # Muestra la proporción de cada categoría dentro del total.
    # Conclusión esperada: qué categoría domina el catálogo de productos económicos.

    crear_ruta_si_no_existe(ruta_destino)

    if lista_colores is None:
        lista_colores = ["#FF9800", "#2196F3", "#4CAF50", "#E91E63", "#9C27B0"]

    figura, area_dibujo = plt.subplots(figsize=(8, 8))
    cantidad_categorias = len(datos_agrupados)

    area_dibujo.pie(
        datos_agrupados[columna_valores],
        labels=datos_agrupados[columna_etiquetas],
        autopct="%1.1f%%",
        colors=lista_colores[:cantidad_categorias],
        startangle=90,
        wedgeprops={"edgecolor": "black", "linewidth": 0.5}
    )

    area_dibujo.set_title(titulo, fontsize=14)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print(f"Gráfico de torta guardado en: {ruta_completa}")


def graficar_mapa_calor(datos_agrupados, columna_filas, columna_columnas, columna_valores,
                        titulo="Mapa de calor", paleta_color="YlOrRd",
                        nombre_archivo="mapa_calor.png", ruta_destino=RUTA_ASSETS):
    # GRÁFICA 4 — Mapa de calor
    # Cruza dos variables categóricas y muestra intensidad por valor.
    # Conclusión esperada: qué producto específico domina en cada categoría premium.

    crear_ruta_si_no_existe(ruta_destino)

    tabla_pivote = datos_agrupados.pivot_table(
        index=columna_filas,
        columns=columna_columnas,
        values=columna_valores,
        aggfunc="sum",
        fill_value=0
    )

    figura, area_dibujo = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        tabla_pivote, annot=True, fmt=".0f",
        cmap=paleta_color, ax=area_dibujo,
        linewidths=0.5, linecolor="gray"
    )

    area_dibujo.set_title(titulo, fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print(f"Mapa de calor guardado en: {ruta_completa}")


def graficar_histograma(data_frame_limpio, columna_valores,
                        titulo="Histograma", color_barras="#9C27B0",
                        nombre_archivo="histograma.png", ruta_destino=RUTA_ASSETS):
    # GRÁFICA 5 — Histograma
    # Muestra cómo se distribuyen los valores de una columna numérica.
    # Conclusión esperada: identificar en qué rango de precios se concentran
    # la mayoría de los productos de la tienda.

    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    # bins=20 divide el rango de precios en 20 intervalos iguales.
    # edgecolor="black" separa visualmente cada barra.
    area_dibujo.hist(
        data_frame_limpio[columna_valores],
        bins=20,
        color=color_barras,
        edgecolor="black"
    )

    area_dibujo.set_title(titulo, fontsize=14)
    area_dibujo.set_xlabel(columna_valores, fontsize=12)
    area_dibujo.set_ylabel("Frecuencia", fontsize=12)
    area_dibujo.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print(f"Histograma guardado en: {ruta_completa}")