# 🧪 Tech Test — FastAPI + PostgreSQL + n8n

## 📋 Descripción del Proyecto

Solución completa de prueba técnica que implementa una API REST con FastAPI, base de datos PostgreSQL, y automatización con n8n. El proyecto incluye:

- **Parte A**: API que consume datos externos con manejo de timeouts y errores
- **Parte B**: Sistema de persistencia con PostgreSQL y SQLAlchemy
- **Parte C**: Flujo automatizado en n8n para procesamiento de datos
- **Parte D**: Meta-prompt para comunicaciones de soporte técnico

## 🏗️ Arquitectura del Proyecto

```
prueba-tecnica-isabella/
├── app/                          # Aplicación principal FastAPI
│   ├── api/routers/              # Endpoints de la API
│   │   ├── external.py          # Consumo de API externa
│   │   └── leads.py             # Gestión de leads
│   ├── db/                      # Configuración de base de datos
│   │   ├── crud_lead.py         # Operaciones CRUD
│   │   ├── init_db.py           # Inicialización de tablas
│   │   └── session.py           # Configuración de sesiones
│   ├── models/                  # Modelos SQLAlchemy
│   │   └── lead.py              # Modelo Lead
│   ├── schemas/                 # Esquemas Pydantic
│   │   └── lead.py              # Validación de datos
│   ├── services/                # Servicios externos
│   │   └── external_client.py   # Cliente HTTP con timeouts
│   └── main.py                  # Aplicación FastAPI
├── scripts/                     # Scripts de utilidad
│   └── seed_leads.py           # Población de datos de ejemplo
├── n8n_flow.json               # Flujo de automatización n8n
├── prompt_example.md           # Meta-prompt de soporte
└── requirements.txt            # Dependencias Python
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.11+** (probado con 3.13.7)
- **Docker Desktop** (para PostgreSQL y n8n)
- **Git** (para clonar el repositorio)

### 1. Configuración del Entorno Virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux (Bash):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno

```bash
copy .env.example .env
```

Edita `.env` y confirma la configuración por defecto:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/leads_db
```

### 4. Configuración de Base de Datos

**Primera vez (crea el contenedor):**

```bash
docker run -d --name techtest-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=leads_db \
  -p 5432:5432 postgres:16
```

**Siguientes veces (ya creado):**

```bash
docker start techtest-postgres
```

### 5. Inicialización de Base de Datos

```bash
# Crear tablas
python -m app.db.init_db

# Opcional: Poblar con datos de ejemplo
python scripts/seed_leads.py
```

### 6. Ejecución de la API

**Opción A (desarrollo con FastAPI CLI):**

```bash
fastapi dev
# Documentación: http://127.0.0.1:8000/docs
```

**Opción B (uvicorn):**

```bash
uvicorn app.main:app --reload
```

## 📊 Funcionalidades de la API

### Endpoints Principales

#### Parte A: Datos Externos

- **GET** `/external-data` - Obtiene datos desde API externa (JSONPlaceholder)
- **POST** `/external-data/filter?limit={n}` - Filtra datos externos por límite

#### Parte B: Gestión de Leads

- **GET** `/leads` - Lista leads con filtros opcionales:
  - `location` - Filtrar por ciudad
  - `min` - Presupuesto mínimo
  - `max` - Presupuesto máximo
- **POST** `/leads` - Crea nuevo lead (JSON: `id`, `name`, `location`, `budget`)

### Modelo de Datos

```python
class Lead:
    id: int          # Identificador único
    name: str        # Nombre del lead (máx. 120 caracteres)
    location: str    # Ciudad (máx. 80 caracteres)
    budget: int      # Presupuesto (entero positivo)
```

## 🔄 Automatización con n8n

### Configuración del Flujo

1. **Levantar n8n:**

```bash
# Primera vez
docker run -d --name n8n -p 5678:5678 \
  -e GENERIC_TIMEZONE=America/Bogota n8nio/n8n:latest

# Siguientes veces
docker start n8n
```

2. **Acceder a la interfaz:** http://localhost:5678

3. **Configurar credenciales PostgreSQL:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `leads_db`
   - User: `postgres`
   - Password: `postgres`

### Flujo de Procesamiento

El flujo n8n implementa la siguiente lógica:

1. **Manual Trigger** → Inicia el proceso
2. **PostgreSQL Query** → Lee todos los leads
3. **IF Filter** → Filtra por:
   - `location == "Bogota"`
   - `budget >= 320000`
   - `budget <= 500000000`
4. **Code Node** → Suma total de presupuestos
5. **Code Node** → Ordena por presupuesto descendente

**Resultado esperado:**

```json
[
  {
    "leads_filtrados": [
      {
        "id": 5,
        "name": "Sofía Ríos",
        "location": "Bogota",
        "budget": 450000
      },
      {
        "id": 3,
        "name": "María Ruiz",
        "location": "Bogota",
        "budget": 320000
      }
    ],
    "total_budget": 770000
  }
]
```

### Importar Flujo Existente

El archivo `n8n_flow.json` contiene el flujo completo. Para importarlo:

1. En n8n: **⋮** → **Import from file**
2. Seleccionar `n8n_flow.json`
3. Configurar credenciales PostgreSQL

## 📝 Meta-prompt de Soporte (Parte D)

El archivo `prompt_example.md` contiene un meta-prompt para generar comunicaciones de soporte técnico en tres estados:

### Estados de Comunicación

1. **Recepción** - Información parcial, solicita datos faltantes
2. **Diagnóstico** - Causa identificada, mitigación en curso
3. **Resolución** - Acciones realizadas, validación y cierre

### Ejemplos de Uso

#### Recepción

```
Asunto: Recepción de tu reporte — necesitamos algunos datos para avanzar
Cuerpo: Gracias por escribirnos. Entendemos que presentas un comportamiento inesperado...
```

#### Diagnóstico

```
Asunto: Diagnóstico inicial — causa detectada y mitigación aplicada
Cuerpo: Analizamos los registros y la configuración relacionada con tu caso...
```

#### Resolución

```
Asunto: Incidencia resuelta — validación final
Cuerpo: Aplicamos las correcciones necesarias y validamos el funcionamiento esperado...
```

## 🔧 Solución de Problemas

### Errores Comunes

**ModuleNotFoundError: No module named 'app'**

- Ejecuta desde la raíz del repositorio
- Asegúrate de tener el entorno virtual activado

**Puerto 5432 ocupado (PostgreSQL)**

```bash
# Usar puerto alternativo
docker run -d --name techtest-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=leads_db \
  -p 5433:5432 postgres:16
```

Actualiza `DATABASE_URL` en `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/leads_db
```

**Docker no responde**

- Abre Docker Desktop
- Espera a que arranque completamente
- Reintenta los comandos

**n8n no carga**

```bash
docker start n8n
# Verifica: http://localhost:5678
```

### Reinicio Completo del Sistema

```bash
# 1. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 2. Iniciar contenedores
docker start techtest-postgres
docker start n8n

# 3. Levantar API
fastapi dev
```

## 📦 Dependencias

### requirements.txt

```
fastapi==0.116.1          # Framework web
fastapi-cli==0.0.10       # CLI para desarrollo
uvicorn==0.35.0           # Servidor ASGI
httpx==0.28.1             # Cliente HTTP asíncrono
SQLAlchemy==2.0.43        # ORM para base de datos
psycopg-binary==3.2.9     # Driver PostgreSQL
```

## 🧪 Pruebas de Aceptación

### Endpoints API

- ✅ GET `/external-data` - Retorna datos externos normalizados
- ✅ POST `/external-data/filter` - Aplica filtros con límite
- ✅ GET `/leads` - Lista con filtros opcionales
- ✅ POST `/leads` - Crea nuevos registros

### Flujo n8n

- ✅ Lectura desde PostgreSQL
- ✅ Filtrado por criterios específicos
- ✅ Cálculo de total de presupuestos
- ✅ Ordenamiento por presupuesto descendente
- ✅ Salida JSON estructurada

### Meta-prompt

- ✅ Generación de comunicaciones de recepción
- ✅ Generación de comunicaciones de diagnóstico
- ✅ Generación de comunicaciones de resolución

---

**Desarrollado por: Isabella Rodríguez Laytón**
