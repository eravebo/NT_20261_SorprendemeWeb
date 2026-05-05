import pandas as pd

# ─────────────────────────────────────────────────────────────
# IMPORTS — EVELYN RAVE (tabla PRODUCTO)
# ─────────────────────────────────────────────────────────────
from utils.simulacion import generar_simulacion
from utils.limpieza   import limpiar_datos
from utils.descripcion import describir_datos

# ─────────────────────────────────────────────────────────────
# IMPORTS — ANDRÉS QUINTERO (tabla PEDIDO)
# ─────────────────────────────────────────────────────────────
from utils.simulacion_pedido  import generar_simulacion_pedido
from utils.limpieza_pedido    import limpiar_datos_pedido
from utils.descripcion_pedido import describir_datos_pedido


# =============================================================
# EVELYN RAVE — tabla PRODUCTO
# =============================================================
print("\n" + "="*60)
print("  EVELYN RAVE — Tabla PRODUCTO")
print("="*60)

simulaciones           = generar_simulacion(1000)
simulaciones_ordenadas = pd.DataFrame(simulaciones)
print(simulaciones_ordenadas)

df_limpio = limpiar_datos(simulaciones_ordenadas)
print(df_limpio)

describir_datos(df_limpio)


# =============================================================
# ANDRÉS QUINTERO — tabla PEDIDO
# =============================================================
print("\n" + "="*60)
print("  ANDRÉS QUINTERO — Tabla PEDIDO")
print("="*60)

df_pedidos_crudo  = generar_simulacion_pedido(1300)
df_pedidos_limpio = limpiar_datos_pedido(df_pedidos_crudo)
describir_datos_pedido(df_pedidos_limpio)
