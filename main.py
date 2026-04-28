import pandas as pd
from utils.descripcion import describir_datos
from utils.simulacion import generar_simulacion
from utils.limpieza import limpiar_datos
from utils.descripcion import describir_datos

simulaciones = generar_simulacion(1000)
simulaciones_ordenadas = pd.DataFrame(simulaciones)
print(simulaciones_ordenadas)

df_limpio = limpiar_datos(simulaciones_ordenadas)
print(df_limpio)

describir_datos(df_limpio)