# API REST USICAMM - Documentación Completa

## Introducción

La API REST de USICAMM permite sincronizar datos entre la aplicación local y la base de datos central.

## Endpoints Principales

### 1. Health Check
**GET** `/api/v1/health`

### 2. Validar Aspirante
**POST** `/api/v1/aspirantes/validar`
```json
{"curp": "ABCD930315HDFRNS09"}
```

### 3. Obtener Resultados
**GET** `/api/v1/examenes/<sesion_id>/resultados`

### 4. Sincronizar
**POST** `/api/v1/sincronizar`

### 5. Listado Nominal
**GET** `/api/v1/listado-nominal?ordenar_por=puntuacion&limite=100`

## Base de Datos Central - PostgreSQL

### Tabla resultados_finales
- id (SERIAL PRIMARY KEY)
- curp (VARCHAR 18, UNIQUE)
- nombre (VARCHAR 100)
- puntuacion (DECIMAL 5,2)
- porcentaje_acierto (DECIMAL 5,2)
- preguntas_correctas (INTEGER)
- preguntas_totales (INTEGER)
- fecha_examen (TIMESTAMP)

### Tabla auditoria_completa
- id (SERIAL PRIMARY KEY)
- tipo_evento (VARCHAR 50)
- descripcion (TEXT)
- curp (VARCHAR 18)
- timestamp (TIMESTAMP)

## Ejemplos cURL

```bash
# Validar aspirante
curl -X POST http://localhost:5000/api/v1/aspirantes/validar \
  -H "Content-Type: application/json" \
  -d '{"curp": "ABCD930315HDFRNS09"}'

# Obtener listado nominal
curl http://localhost:5000/api/v1/listado-nominal?limite=50
```
