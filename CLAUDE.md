# CLAUDE.md — NT_20261_SorprendemeWeb

Contexto del proyecto para Claude Code. Léelo antes de cualquier tarea.

## Descripción del proyecto

SorpréndemeWeb es el proyecto integrador de la materia NT_20261 (martes).
Es una tienda de regalos de Medellín que aún no tiene presencia digital consolidada.
El proyecto construye el pipeline de datos y el frontend de análisis.

## Integrantes y responsabilidades

| Integrante | Tabla | Rama principal |
|---|---|---|
| Evelyn Rave | PRODUCTO | sus propias ramas |
| Andrés Quintero | PEDIDO | `andres/pedido-pipeline` |

**Regla crítica:** No modificar el código de Evelyn (tabla PRODUCTO) a menos que sea estrictamente necesario para que el programa funcione. Siempre agregar código nuevo debajo o aparte del suyo.

## Repositorios

- **Pipeline de datos (este repo):** `https://github.com/eravebo/NT_20261_SorprendemeWeb`
- **Frontend React:** `https://github.com/eravebo/Sorprendeme_integrador_front`
- **Backend Spring Boot:** carpeta local `Sorprendeme_integrador_backend` (no tiene repo propio aún)

## Estructura del proyecto

```
NT_20261_SorprendemeWeb/
├── main.py                        # Punto de entrada — corre el pipeline completo
├── requirements.txt               # Dependencias Python
├── utils/
│   ├── simulacion.py              # EVELYN — genera dataset PRODUCTO (1000 registros)
│   ├── limpieza.py                # EVELYN — limpia dataset PRODUCTO
│   ├── descripcion.py             # EVELYN — análisis exploratorio PRODUCTO
│   ├── transformacion.py          # EVELYN — agrupa y exporta JSONs PRODUCTO
│   ├── graficacion.py             # COMPARTIDO — funciones de graficación (lineas, barras, torta, calor, histograma)
│   ├── consumo.py                 # COMPARTIDO — conecta al backend Spring Boot (GET /api/productos y /api/pedidos)
│   ├── simulacion_pedido.py       # ANDRÉS — genera dataset PEDIDO (1300 registros)
│   ├── limpieza_pedido.py         # ANDRÉS — limpia dataset PEDIDO
│   ├── descripcion_pedido.py      # ANDRÉS — análisis exploratorio PEDIDO
│   ├── transformacion_pedido.py   # ANDRÉS — agrupa y exporta JSONs PEDIDO
│   └── graficacion_pedido.py      # ANDRÉS — llama a graficacion.py con parámetros de pedidos
├── BD_Simulacion/                 # Datos crudos generados (en .gitignore)
├── BD_Limpieza/                   # Datos limpios (en .gitignore)
├── BD_Analisis/                   # JSONs de agrupaciones para el frontend
│   ├── anchetas_por_fecha.json
│   ├── productos_premium_por_categoria.json
│   ├── productos_economicos_por_categoria.json
│   ├── distribucion_general.json
│   ├── calor_categoria_nombre.json
│   ├── stock_bajo_por_categoria.json
│   ├── pedidos_por_fecha.json
│   ├── pedidos_por_estado.json
│   ├── pedidos_aprobados_por_mes.json
│   ├── pedidos_estado_por_mes.json
│   ├── distribucion_mp_status.json
│   └── distribucion_pedidos_general.json
├── frontend/src/assets/graficos/  # PNGs generados por matplotlib/seaborn
└── logs/                          # Reportes de limpieza y descripción
```

## Cómo correr el pipeline

```bash
# Activar entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Instalar dependencias (solo la primera vez)
pip install -r requirements.txt
pip install matplotlib seaborn

# Correr el pipeline completo
python main.py
# En Windows con emoji en consola:
$env:PYTHONUTF8="1"; venv\Scripts\python.exe main.py
```

**Outputs:**
- `BD_Analisis/*.json` — datos para React
- `frontend/src/assets/graficos/*.png` — gráficas estáticas

## Stack completo para correr la aplicación

1. **XAMPP** — iniciar Apache + MySQL
2. **IntelliJ** — correr el backend Spring Boot (`Sorprendeme_integrador_backend/`) en puerto `8080`
3. **React** — en `Sorprendeme_integrador_front/`: `npm install` (primera vez) y `npm start` → `localhost:3000`

## Pipeline PEDIDO — detalle (Andrés)

### Columnas del dataset
`id, nombre_cliente, telefono, email, direccion_envio, fecha, estado, mp_payment_id, mp_status`

### Estados posibles
- `estado`: `aprobado` (55%), `pendiente` (30%), `rechazado` (15%)
- `mp_status`: `approved`, `pending`, `rejected`, `Sin procesar`

### Datos sucios intencionales en simulación
- IDs duplicados (~15%)
- Fechas en 4 formatos distintos (`%Y-%m-%d %H:%M`, `%d/%m/%Y %H:%M`, etc.)
- Nulos en `mp_payment_id` y `mp_status` para pedidos pendientes

### JSONs exportados por `transformacion_pedido.py`
| Archivo | Contenido | Gráfica |
|---|---|---|
| `pedidos_por_fecha.json` | `{fecha_dia, conteo}` | Línea |
| `pedidos_por_estado.json` | `{estado, conteo}` | Barras |
| `pedidos_estado_por_mes.json` | `{mes, estado, conteo}` | Mapa de calor |
| `pedidos_aprobados_por_mes.json` | `{mes, conteo}` | Barras |
| `distribucion_mp_status.json` | `{mp_status, conteo}` | Torta |
| `distribucion_pedidos_general.json` | `{estado, conteo}` | KPI total |

## Frontend — Dashboard

**Archivo principal:** `Sorprendeme_integrador_front/src/pages/Dashboard/Dashboard.js`

- Sección PRODUCTO (Evelyn): KPIs + 5 gráficas (línea, barras, torta, mapa calor PNG, histograma PNG)
- Sección PEDIDO (Andrés): KPIs + 5 gráficas (línea, torta, barras, mapa calor PNG, histograma PNG)
- Datos dinámicos: se cargan desde `public/data/*.json` con `fetch`
- Datos estáticos: PNG importados desde `src/assets/graficos/`
- Librería de gráficas: **Recharts**
- Paleta: `#ec3d6c` (rosa primario), `#f77fa0` (acento), `#f5b5c1` (secundario)

## Convenciones

- Responder siempre en **español**
- Ramas de Andrés: prefijo `andres/`
- Branch principal de trabajo: `develop`
- Commits: formato `feat(scope):`, `fix(scope):`, etc.
- No commitear archivos de `BD_Limpieza/` ni `BD_Simulacion/` (están en `.gitignore`)
