import random
from datetime import datetime, timedelta
import os
import pandas as pd
from faker import Faker

fake = Faker('es_CO')
random.seed(42)


def generar_simulacion_pedidos(numero_simulaciones):

    ESTADOS = ['pendiente', 'aprobado', 'rechazado']
    MP_ESTADOS = ['approved', 'pending', 'rejected', 'in_process']
    FORMATOS_FECHA = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M', '%d-%m-%Y', '%Y/%m/%d']

    simulaciones = []

    for i in range(numero_simulaciones):
        estado = random.choice(ESTADOS)

        # mp_payment_id y mp_status solo existen si paso por MercadoPago
        tiene_pago = random.random() > 0.25
        mp_payment_id = f'MP-{random.randint(100000, 9999999)}' if tiene_pago else None
        mp_status = random.choice(MP_ESTADOS) if tiene_pago else None

        fecha_inicio = datetime(2024, 1, 1)
        dias_random = random.randint(0, 730)
        hora_random = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        fecha = fecha_inicio + timedelta(days=dias_random) + hora_random
        formato = random.choice(FORMATOS_FECHA)
        fecha_texto = fecha.strftime(formato)

        simulacion = {
            'id': i + 1,
            'nombre_cliente': fake.name(),
            'telefono': fake.numerify(text='3########'),
            'email': fake.email(),
            'direccion_envio': fake.address().replace('\n', ', '),
            'fecha': fecha_texto,
            'estado': estado,
            'mp_payment_id': mp_payment_id,
            'mp_status': mp_status,
        }

        # Inyeccion de errores intencionales (~30% de registros)
        probabilidad_error = random.random()

        if probabilidad_error < 0.05:
            # ID invalido
            simulacion['id'] = random.choice([None, -1, 0])
        elif probabilidad_error < 0.12:
            # Nombre en mayusculas (error de formato)
            simulacion['nombre_cliente'] = simulacion['nombre_cliente'].upper()
        elif probabilidad_error < 0.18:
            # Estado con capitalizacion incorrecta
            simulacion['estado'] = simulacion['estado'].title()
        elif probabilidad_error < 0.22:
            # Email malformado (sin @)
            simulacion['email'] = simulacion['email'].replace('@', '')
        elif probabilidad_error < 0.26:
            # Telefono con texto mezclado
            simulacion['telefono'] = f"Tel: {simulacion['telefono']}"
        elif probabilidad_error < 0.30:
            # Nombre con espacios extra
            simulacion['nombre_cliente'] = f"  {simulacion['nombre_cliente']}  "

        simulaciones.append(simulacion)

    # Exportar
    os.makedirs('BD_Simulacion', exist_ok=True)
    df = pd.DataFrame(simulaciones)
    df.to_csv('BD_Simulacion/pedidos_dataset.csv', index=False, encoding='utf-8-sig', sep=';')
    df.to_json('BD_Simulacion/pedidos_dataset.json', orient='records', force_ascii=False, indent=2)

    print(f'Simulacion completada. Registros generados: {df.shape[0]}')
    return simulaciones


if __name__ == '__main__':
    datos = generar_simulacion_pedidos(1000)
    df = pd.DataFrame(datos)
    print(df.head(10).to_string())