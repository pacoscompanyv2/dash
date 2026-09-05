# Sales Analytics Dashboard

Dashboard interactivo (Streamlit + PostgreSQL + Docker) sobre `SalesRecords.csv` (100,000 registros de ventas globales).

## Estructura

```
.
├── app/
│   ├── app.py        # Dashboard Streamlit (sidebar, KPIs, gráficas)
│   ├── db.py          # Conexión a PostgreSQL
│   └── queries.py     # Consultas SQL
├── db/
│   ├── schema.sql      # Tabla sales + índices + vista
│   └── load_data.py    # Carga el CSV a PostgreSQL (idempotente)
├── data/
│   └── SalesRecords.csv
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── .env.example
└── .streamlit/config.toml
```

## Correrlo local

1. Copia las variables de entorno:
   ```
   cp .env.example .env
   ```
2. Levanta todo con Docker:
   ```
   docker compose up --build
   ```
3. Abre http://localhost:8501

Para apagarlo: `Ctrl + C` y luego `docker compose down` (agrega `-v` para borrar los datos cargados).

## Deploy en Render

1. Sube este proyecto a tu repo de GitHub.
2. En Render, crea un nuevo Blueprint apuntando al repo (Render detecta `render.yaml` automáticamente y crea la base de datos y el servicio web).
3. Espera el build y Render te da tu URL pública.
