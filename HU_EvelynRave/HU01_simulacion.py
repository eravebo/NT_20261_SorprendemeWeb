import random
import json
import pandas as pd
from faker import Faker
import os

fake = Faker('es_CO')
random.seed(42)
Faker.seed(42)

CATEGORIAS = ['ancheta', 'flores', 'peluche']
NOMBRES = {
    'ancheta': ['Ancheta Romántica', 'Ancheta Termo GYM', 'Ancheta con Peluche y frutas'],
    'flores':  ['Ramo de Rosas', 'Bouquet con Girasoles', 'Ramo Sencillo'],
    'peluche': ['Peluche Lucifer', 'Conejo Grande', 'Panda Pequeño']
}

registros = []
ids_generados = []

for i in range(1300):
    categoria = random.choice(CATEGORIAS)

    nombre_base = random.choice(NOMBRES[categoria])
    transformacion = random.choice(['original', 'mayusculas', 'minusculas'])
    
    if transformacion == 'mayusculas':
        nombre_final = nombre_base.upper()
    elif transformacion == 'minusculas':
        nombre_final = nombre_base.lower()
    else:
        nombre_final = nombre_base
        
    if ids_generados and random.random() < 0.15:
        nuevo_id = random.choice(ids_generados)
    else:
        nuevo_id = random.randint(1, 9999)
    ids_generados.append(nuevo_id)

    FORMATOS_FECHA = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']

    registro = {
        'id': nuevo_id,
        'nombre': nombre_final,
        'descripcion': fake.text(max_nb_chars=150) if random.random() > 0.20 else None,
        'precio': round(random.uniform(15000, 350000), 2),
        'categoria': categoria,
        'imagen_url': f"https://sorprendeme.com/img/{categoria}/{nuevo_id}.jpg",
        'stock': random.randint(0, 200),
        'fecha_creacion': fake.date_between(start_date='-2y', end_date='today').strftime(random.choice(FORMATOS_FECHA))
    }
    registros.append(registro)

os.makedirs("HU_EvelynRave/BD_Simulacion", exist_ok=True)
df = pd.DataFrame(registros)
df.to_csv('HU_EvelynRave/BD_Simulacion/productos_dataset.csv', index=False, encoding='utf-8-sig', sep=';')
df.to_json('HU_EvelynRave/BD_Simulacion/productos_dataset.json', orient='records', force_ascii=False, indent=2)

df_csv = pd.read_csv('HU_EvelynRave/BD_Simulacion/productos_dataset.csv', encoding='utf-8-sig', sep=';')
df_json = pd.read_json('HU_EvelynRave/BD_Simulacion/productos_dataset.json')

print(df.shape)
print(df_csv.shape)
print(df_json.shape)