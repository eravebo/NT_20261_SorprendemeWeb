import random
from datetime import datetime, timedelta
import os
import pandas as pd

random.seed(42)

def generar_simulacion(numeroSimulaciones):
    
    CATEGORIAS = ['ancheta', 'flores', 'peluche']
    
    NOMBRES = {
        'ancheta': ['Ancheta Romántica', 'Caja de Amor', 'Ancheta Premium', 'Canasta Especial'],
        'flores':  ['Rosas Rojas', 'Bouquet Mixto', 'Girasoles', 'Liliums Blancos'],
        'peluche': ['Oso de Peluche', 'Conejo Gigante', 'Panda Suave', 'Unicornio']
    }
    
    FORMATOS_FECHA = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']
    
    simulaciones = []
    ids_generados = []
    
    for _ in range(numeroSimulaciones):
        categoria = random.choice(CATEGORIAS)
        nombre = random.choice(NOMBRES[categoria])
        
        fecha_inicio = datetime(2024, 1, 1)
        dias_random = random.randint(0, 730)
        fecha = fecha_inicio + timedelta(days=dias_random)
        formato = random.choice(FORMATOS_FECHA)
        fecha_texto = fecha.strftime(formato)
        
        simulacion = {
            'id': random.randint(1, 9999),
            'nombre': nombre,
            'descripcion': random.choice(['Producto especial', 'Edición limitada', 'Más vendido', None]),
            'precio': round(random.uniform(15000, 350000), 0),
            'categoria': categoria,
            'imagen_url': f'https://sorprendeme.com/img/{categoria}/{random.randint(1,999)}.jpg',
            'stock': random.randint(0, 200),
            'fecha_creacion': fecha_texto
        }
        probabilidadError = random.random()

        if probabilidadError < 0.1:
            simulacion['id'] = random.choice([None, -1, 0])
        elif probabilidadError < 0.3:
            simulacion['nombre'] = simulacion['nombre'].upper()
        elif probabilidadError < 0.6:
            simulacion['categoria'] = simulacion['categoria'].title()

        simulaciones.append(simulacion)
    
    os.makedirs('BD_Simulacion', exist_ok=True)

    df = pd.DataFrame(simulaciones)
    df.to_csv('BD_Simulacion/productos_dataset.csv', index=False, encoding='utf-8-sig', sep=';')
    df.to_json('BD_Simulacion/productos_dataset.json', orient='records', force_ascii=False, indent=2)

    return simulaciones
