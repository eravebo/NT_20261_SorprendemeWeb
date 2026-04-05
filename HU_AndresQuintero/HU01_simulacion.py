import random
import pandas as pd
import os
from datetime import datetime, timedelta

# ============================================================
# HU 01 - Simulación y exportación de datos de la tabla PEDIDO
# Proyecto Integrador: SorpréndemeWeb - Tienda de regalos Medellín
# Integrante: Andrés Quintero
# ============================================================
# Como desarrollador de soluciones de datos
# quiero simular un conjunto de datos en Python y exportarlo en formatos CSV y JSON
# para disponer de información de prueba reutilizable en distintos escenarios.
# ============================================================

random.seed(42)

# --- Datos de prueba realistas para una tienda de regalos en Medellín ---

NOMBRES = [
    "Valentina García", "Santiago Martínez", "Camila López", "Sebastián Rodríguez",
    "Isabella Hernández", "Mateo González", "Sofía Torres", "Samuel Díaz",
    "Mariana Ramírez", "Tomás Vargas", "Lucía Castro", "Nicolás Moreno",
    "Salomé Jiménez", "Alejandro Ruiz", "Gabriela Pérez", "Daniel Reyes",
    "Manuela Sánchez", "Juan Pablo Gómez", "Sara Álvarez", "Esteban Ramos",
    "Paula Mendoza", "Andrés Herrera", "María José Suárez", "Felipe Ríos",
    "Ana Lucía Medina", "Diego Cardona", "Laura Gutiérrez", "Julián Ortiz",
    "Natalia Vega", "Cristian Muñoz"
]

PREFIJOS_TEL = ["300", "301", "302", "304", "305", "310", "311", "312",
                "313", "314", "315", "316", "317", "318", "320"]

DOMINIOS_EMAIL = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

BARRIOS = [
    "Laureles", "El Poblado", "Belén", "Envigado", "Sabaneta",
    "Itagüí", "Robledo", "Aranjuez", "Manrique", "Buenos Aires",
    "La América", "Guayabal", "San Javier", "Castilla", "Doce de Octubre",
    "La Candelaria", "Bello", "Copacabana", "Girardota", "Caldas"
]

CALLES = ["Cra", "Cl", "Av", "Diagonal", "Transversal"]

ESTADOS = ["pendiente", "aprobado", "rechazado"]
PESOS_ESTADO = [0.30, 0.55, 0.15]

FORMATOS_FECHA = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']


def generar_telefono():
    prefijo = random.choice(PREFIJOS_TEL)
    numero = "".join([str(random.randint(0, 9)) for _ in range(7)])
    return f"+57 {prefijo} {numero[:3]} {numero[3:]}"


def generar_email(nombre):
    partes = nombre.lower().split()
    base = f"{partes[0]}.{partes[-1]}" if len(partes) > 1 else partes[0]
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u")]:
        base = base.replace(a, b)
    dominio = random.choice(DOMINIOS_EMAIL)
    return f"{base}{random.randint(1, 999)}@{dominio}"


def generar_direccion():
    calle = random.choice(CALLES)
    n1 = random.randint(1, 120)
    n2 = random.randint(1, 99)
    n3 = random.randint(1, 50)
    barrio = random.choice(BARRIOS)
    return f"{calle} {n1} #{n2}-{n3}, {barrio}, Medellín"


def generar_fecha():
    inicio = datetime(2022, 1, 1)
    fin = datetime(2024, 12, 31)
    fecha = inicio + timedelta(days=random.randint(0, (fin - inicio).days))
    fecha = fecha.replace(hour=random.randint(8, 22), minute=random.randint(0, 59), second=0)
    return fecha.strftime(random.choice(FORMATOS_FECHA))


def generar_mp_payment_id(estado):
    if estado in ["aprobado", "rechazado"]:
        return str(random.randint(10000000000, 99999999999))
    return None


def generar_mp_status(estado):
    if estado == "aprobado":
        return "approved"
    elif estado == "rechazado":
        return "rejected"
    else:
        return random.choice(["pending", None])


# --- Generación del dataset con IDs con posibles duplicados (igual que Evelyn) ---
registros = []
ids_generados = []

for i in range(1300):
    nombre = random.choice(NOMBRES)
    estado = random.choices(ESTADOS, weights=PESOS_ESTADO)[0]

    if ids_generados and random.random() < 0.15:
        nuevo_id = random.choice(ids_generados)
    else:
        nuevo_id = random.randint(1, 9999)
    ids_generados.append(nuevo_id)

    registro = {
        "id": nuevo_id,
        "nombre_cliente": nombre,
        "telefono": generar_telefono(),
        "email": generar_email(nombre),
        "direccion_envio": generar_direccion(),
        "fecha": generar_fecha(),
        "estado": estado,
        "mp_payment_id": generar_mp_payment_id(estado),
        "mp_status": generar_mp_status(estado)
    }
    registros.append(registro)
    ids_generados.append(nuevo_id)

# --- Crear DataFrame y exportar ---
os.makedirs("HU_AndresQuintero/BD_Simulacion", exist_ok=True)
df = pd.DataFrame(registros)

# Exportar con el mismo formato que Evelyn: sep=';' y encoding='utf-8-sig'
ruta_csv = "HU_AndresQuintero/BD_Simulacion/pedidos_dataset.csv"
ruta_json = "HU_AndresQuintero/BD_Simulacion/pedidos_dataset.json"

df.to_csv(ruta_csv, index=False, encoding='utf-8-sig', sep=';')
df.to_json(ruta_json, orient='records', force_ascii=False, indent=2)

# --- Verificación (igual que Evelyn) ---
df_csv = pd.read_csv(ruta_csv, encoding='utf-8-sig', sep=';')
df_json = pd.read_json(ruta_json)

print(df.shape)
print(df_csv.shape)
print(df_json.shape)
