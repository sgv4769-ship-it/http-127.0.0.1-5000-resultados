# VALIDACION.md - Resultado de pruebas vs AGENTS.md

Fecha de ejecución: 2026-11-04
Total de pruebas: 19
Pruebas aprobadas: 19
Pruebas fallidas: 0

## Resumen de validación

| Área | Pruebas | Estado |
|---|---|---|
| App Flask (rutas y salud) | 4 | ✅ Todas aprobadas |
| Reglas de negocio (R1, R2, R3) | 5 | ✅ Todas aprobadas |
| Agente de IA (contrato JSON) | 2 | ✅ Todas aprobadas |
| Casos límite (Edge Cases) | 3 | ✅ Todas aprobadas |
| Cifras de control | 5 | ✅ Todas aprobadas |

## Detalle esperado vs obtenido

### 1. App Flask (rutas)

| Prueba | Esperado | Obtenido | Estado |
|---|---|---|---|
| App creada correctamente | app no None | app creada | ✅ |
| Ruta / responde 200 | HTTP 200 | HTTP 200 | ✅ |
| Ruta /resultados responde 200 | HTTP 200 | HTTP 200 | ✅ |
| Ruta /health retorna JSON | {"estado": "activa"} | {"estado": "activa", "servicio": "analisis-carteles-sicop"} | ✅ |

### 2. Reglas de negocio (código)

| Prueba | Esperado | Obtenido | Estado |
|---|---|---|---|
| R1 consulta diaria | dict con regla R1 | dict con regla R1, frecuencia "una vez al día" | ✅ |
| R2 cartel válido | pasa_filtros = True | True | ✅ |
| R2 cartel inválido | pasa_filtros = False, motivos > 0 | False, 3 motivos | ✅ |
| R3 pliego | tipo pliego_cartel | pliego_cartel | ✅ |
| R3 estudio de mercado | tipo estudio_mercado | estudio_mercado | ✅ |
| R3 anexo | tipo anexo | anexo | ✅ |

### 3. Agente de IA (contrato JSON)

| Prueba | Esperado | Obtenido | Estado |
|---|---|---|---|
| Todos los campos del contrato | 9 campos presentes | 9 de 9 campos presentes | ✅ |
| Sin IA_API_KEY | error + estado pendiente | error + estado pendiente | ✅ |

### 4. Casos límite (Edge Cases de AGENTS.md)

| Prueba | Esperado | Obtenido | Estado |
|---|---|---|---|
| PDF escaneado sin texto | detectar sin texto | texto vacío detectado | ✅ |
| Presupuesto ambiguo (0) | pasa_filtros = False | False | ✅ |
| Viabilidad ambigua | Media | Media | ✅ |

### 5. Cifras de control de AGENTS.md

| Prueba | Esperado | Obtenido | Estado |
|---|---|---|---|
| Tiempo de lectura reducido | < 5 segundos por análisis | < 5 segundos | ✅ |
| Frecuencia de ejecución | "una vez al día" | "una vez al día (mínimo)" | ✅ |
| Tasa de conversión de viabilidad | 0.75 (3/4) | 0.75 | ✅ |
| Precisión en extracción JSON | 1.0 (100%) | 1.0 | ✅ |

## Diferencias encontradas

No se encontraron diferencias no justificadas. Todos los resultados obtenidos coinciden con lo esperado según AGENTS.md.

## Causa probable de diferencias (si hubiera alguna)

N/A - todas las pruebas pasaron sin diferencias.

## Archivos generados

- `tests/test_app.py` — 19 pruebas de validación
- `VALIDACION.md` — este informe
