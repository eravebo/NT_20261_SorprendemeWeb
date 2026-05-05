import random
import pandas as pd
import os
from datetime import datetime, timedelta

random.seed(42)

NOMBRES_CLIENTES = [
    "Valentina García", "Santiago Martínez", "Camila López", "Sebastián Rodríguez",
    "Isabella Hernández", "Mateo González", "Sofía Torres", "Samuel Díaz",
    "Mariana Ramírez", "Tomás Vargas", "Lucía Castro", "Nicolás Moreno",
    "Salomé Jiménez", "Alejandro Ruiz", "Gabriela Pérez", "Daniel Reyes",
    "Manuela Sánchez", "Juan Pablo Gómez", "Sara Álvarez", "Esteban Ramos",
    "Paula Mendoza", "Andrés Herrera", "María José Suárez", "Felipe Ríos",
    "Ana Lucía Medina", "Diego Cardona", "Laura Gutiérrez", "Julián Ortiz",
    "Natalia Vega", "Cristian Muñoz"
]

PREFIJOS_TEL   = ["300","301","302","304","305","310","311","312","313","314","315","316","317","318","320"]
DOMINIOS_EMAIL = ["gmail.com","hotmail.com","yahoo.com","outlook.com"]
BARRIOS        = ["Laureles","El Poblado","Belén","Envigado","Sabaneta","Itagüí","Robledo",
                  "Aranjuez","Manrique","Buenos Aires","La América","Guayabal","San Javier",
                  "Castilla","Doce de Octubre","La Candelaria","Bello","Copacabana","Girardota","Caldas"]
CALLES         = ["Cra","Cl","Av","Diagonal","Transversal"]
ESTADOS        = ["pendiente","aprobado","rechazado"]
PESOS_ESTADO   = [0.30, 0.55, 0.15]
FORMATOS_FECHA = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']


def _generar_telefono():
    prefijo = random.choice(PREFIJOS_TEL)
    numero  = "".join([str(random.randint(0, 9)) for _ in range(7)])
    return f"+57 {prefijo} {numero[:3]} {numero[3:]}"


def _generar_email(nombre):
    partes = nombre.lower().split()
    base   = f"{partes[0]}.{partes[-1]}" if len(partes) > 1 else partes[0]
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u")]:
        base = base.replace(a, b)
    return f"{base}{random.randint(1,999)}@{random.choice(DOMINIOS_EMAIL)}"


def _generar_direccion():
    return (f"{random.choice(CALLES)} {random.randint(1,120)} "
            f"#{random.randint(1,99)}-{random.randint(1,50)}, "
            f"{random.choice(BARRIOS)}, Medellín")


def _generar_fecha():
    inicio = datetime(2022, 1, 1)
    fin    = datetime(2024, 12, 31)
    fecha  = inicio + timedelta(days=random.randint(0, (fin - inicio).days))
    fecha  = fecha.replace(hour=random.randint(8,22), minute=random.randint(0,59), second=0)
    return fecha.strftime(random.choice(FORMATOS_FECHA))


def _generar_mp_payment_id(estado):
    return str(random.randint(10000000000, 99999999999)) if estado in ["aprobado","rechazado"] else None


def _generar_mp_status(estado):
    if estado == "aprobado":  return "approved"
    if estado == "rechazado": return "rejected"
    return random.choice(["pending", None])


def generar_simulacion_pedido(numero_simulaciones=1300):
    """
    HU 01 PEDIDO — Genera dataset sintético de pedidos de SorpréndemeWeb.
    Introduce IDs duplicados (~15%) y fechas en 4 formatos como datos sucios intencionales.
    Exporta a BD_Simulacion/pedidos_dataset.csv y .json
    """
    registros     = []
    ids_generados = []

    for _ in range(numero_simulaciones):
        nombre = random.choice(NOMBRES_CLIENTES)
        estado = random.choices(ESTADOS, weights=PESOS_ESTADO)[0]

        if ids_generados and random.random() < 0.15:
            nuevo_id = random.choice(ids_generados)
        else:
            nuevo_id = random.randint(1, 9999)
        ids_generados.append(nuevo_id)

        registros.append({
            "id"             : nuevo_id,
            "nombre_cliente" : nombre,
            "telefono"       : _generar_telefono(),
            "email"          : _generar_email(nombre),
            "direccion_envio": _generar_direccion(),
            "fecha"          : _generar_fecha(),
            "estado"         : estado,
            "mp_payment_id"  : _generar_mp_payment_id(estado),
            "mp_status"      : _generar_mp_status(estado)
        })

    os.makedirs("BD_Simulacion", exist_ok=True)
    df = pd.DataFrame(registros)
    df.to_csv("BD_Simulacion/pedidos_dataset.csv",  index=False, encoding="utf-8-sig", sep=";")
    df.to_json("BD_Simulacion/pedidos_dataset.json", orient="records", force_ascii=False, indent=2)

    return df
