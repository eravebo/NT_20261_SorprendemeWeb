import requests
import pandas as pd

# Este módulo obtiene los datos de productos desde el backend Spring Boot
# y los convierte en un DataFrame listo para limpiar y analizar.
#
# Flujo completo:
#   consumo.py → limpieza.py → descripcion.py → transformacion.py → graficacion.py
#
# El backend debe estar corriendo en localhost:8080 antes de ejecutar.

BASE_URL = "http://localhost:8080"


def consumir_productos():
    """
    Llama al endpoint GET /api/productos del backend Spring Boot,
    convierte la respuesta JSON en un DataFrame de pandas y lo retorna.

    Columnas esperadas: id, nombre, descripcion, precio, categoria,
                        imagen_url, stock, fecha_creacion
    """
    url = f"{BASE_URL}/api/productos"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()

        datos = respuesta.json()
        data_frame = pd.DataFrame(datos)

        print(f"Conexión exitosa. Registros recibidos: {len(data_frame)}")
        return data_frame

    except requests.exceptions.ConnectionError:
        print("ERROR: No se pudo conectar al backend.")
        print(f"Verifica que Spring Boot esté corriendo en {BASE_URL}")
        return None

    except requests.exceptions.HTTPError as error_http:
        print(f"ERROR HTTP: {error_http}")
        print("Verifica que el endpoint /api/productos exista en el backend.")
        return None

    except Exception as error_general:
        print(f"ERROR inesperado: {error_general}")
        return None


def consumir_productos_desde_json(ruta_archivo="BD_Simulacion/productos_dataset.json"):
    """
    Alternativa local: carga los datos desde un archivo JSON en disco.
    Úsala cuando el backend no esté disponible o para pruebas rápidas.
    """
    try:
        data_frame = pd.read_json(ruta_archivo)
        print(f"Archivo cargado. Registros: {len(data_frame)}")
        return data_frame

    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo: {ruta_archivo}")
        print("Primero corre generar_simulacion() para crear los datos de prueba.")
        return None

    except Exception as error_general:
        print(f"ERROR al leer el archivo: {error_general}")
        return None