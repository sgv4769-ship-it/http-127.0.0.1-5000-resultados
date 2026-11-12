# PLAN.md - Plan de entregas del proyecto

## 1. RESUMEN (5 líneas)
Vamos a construir una app web de automatización e IA para TI – Preventa Comercial que se conecta al portal SICOP de Costa Rica, descarga y analiza Pliegos de Condiciones (TDR/Carteles), y emite una recomendación de viabilidad. Entra: PDF descargados de SICOP (datos de entrada) y 3 PDFs de referencia normativa en `insumos`. El agente de IA lee el cartel y devuelve un JSON con campos como `numero_cartel`, `presupuesto_estimado`, `viabilidad_participacion`, etc. Sale: documento de entendimiento del TDR, alertas/notificaciones a verticales de negocio, y pantalla web con contadores y tabla de resultados.

## 2. LO QUE ENCONTRÉ
**Contexto (`contexto/`):**
- `Contexto_Mi_App.md` con las 8 secciones del contexto (qué es la app, reglas de negocio, contrato JSON, qué produce, quién decide, cifras de control, casos límite, reglas del sistema).
- `Resumen y Prompts de Agentes - Licitaciones Costa Rica.pdf` (presente en la carpeta, no analizado como dato de entrada).

**Insumos (`insumos/`):**
- `Ley_N__9986_Reglamento_Ley_General_de_Contratación_Pública.pdf` — 190 páginas, 190/190 con texto. Reglamento LGCP (Ley 9986). Referencia normativa.
- `ley-general-contratacion-publica-9986.pdf` — 97 páginas, 97/97 con texto. Ley General de Contratación Pública No. 9986. Referencia normativa.
- `Pliego de condiciones - Adquisición de un WAF (2).pdf` — 19 páginas, 19/19 con texto. Licitación reducida BANHVI para WAF Administrado. Ejemplo de pliego/cartel.
- Ninguno tiene columnas ni filas (son PDF, no Excel/CSV).
- Ninguno es un cartel de SICOP con datos estructurados de entrada.

**¿Coincide con AGENTS.md?**
Sí, parcialmente. AGENTS.md establece que los datos de entrada son PDF descargados de SICOP y que los insumos son referencia normativa. Lo que se encuentra coincide con eso.

**Qué falta o no cuadra:**
- No existen archivos Excel/CSV con carteles de SICOP (columnas como `numero_cartel`, `presupuesto_estimado`, `moneda`, `fecha_limite_presentacion`). Esos campos solo aparecen como **salida** del contrato JSON del agente, no como entrada estructurada.
- No existe archivo `.env` con la llave de la IA.
- No existe estructura Flask (`app/`, `wsgi.py`, `iniciar_app.bat`).
- No existen pruebas en `tests/` ni `VALIDACION.md`.
- No existe `PLAN.md` (este archivo lo estoy creando).

## 3. ENTREGAS POR SUBAGENTE (orden de ejecución)

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|---|---|---|---|---|---|
| 1 | @arquitecto | PLAN.md aprobado por el usuario | `PLAN.md` | AGENTS.md, `contexto/`, `insumos/` | Este PLAN.md leído y aprobado por el usuario |
| 2 | @backend | Estructura MVC base con uv: `create_app()`, `wsgi.py`, `iniciar_app.bat`, `.env.example`, carpeta `app/` con `__init__.py`, `controllers/` y `services/` vacíos | `app/__init__.py`, `app/controllers/`, `app/services/`, `wsgi.py`, `iniciar_app.bat`, `.env.example` | PLAN.md aprobado | Ejecutar `iniciar_app.bat` y ver que abre el navegador con la app Flask corriendo (pantalla en blanco o 404 de rutas) |
| 3 | @backend | Regla R1: Conexión periódica y descarga — función `consultar_sicop_diario()` en `services/` con comentario | `app/services/regla1_descarga.py` (o similar) | Estructura MVC base (entrega 2) | Ejecutar la función y ver en consola/print que simula la consulta diaria a SICOP |
| 4 | @backend | Regla R2: Filtros duros iniciales — función `aplicar_filtros_duros()` en `services/` con comentario (rango presupuesto, plazos, industria TI) | `app/services/regla2_filtros.py` | Entrega 3 (R1) | Pasar un cartel de ejemplo y ver en pantalla si pasa o no los filtros duros |
| 5 | @backend | Regla R3: Inventario y enrutamiento — función `clasificar_y_enrutar_documento()` en `services/` con comentario | `app/services/regla3_inventario.py` | Entrega 4 (R2) | Pasar un PDF de insumos y ver en pantalla a qué carpeta del repositorio central se enruta |
| 6 | @backend | Integración agente de IA: función `analizar_con_agente_ia()` en `services/` que lee la llave de `.env`, llama al agente y devuelve el contrato JSON completo | `app/services/agente_ia.py` | Entrega 5 (R3) | Pasar el pliego WAF de insumos y ver en pantalla el JSON válido con todos los campos del contrato |
| 7 | @frontend | Pantalla de inicio: `base.html` (CSS embebido, fondo oscuro, estilo profesional, sin JS externo) y `inicio.html` | `app/templates/base.html`, `app/templates/inicio.html` | Estructura MVC base (entrega 2) | Abrir `iniciar_app.bat` y ver la pantalla de inicio cargando en el navegador |
| 8 | @frontend | Pantalla de resultados: `resultados.html` con tablero de contadores grandes y tabla con filtro, más detalle por registro | `app/templates/resultados.html` | Entrega 7 (inicio) | Abrir la app y ver contadores grandes, tabla filtratable y botón de detalle por registro |
| 9 | @tester | Pruebas en `tests/` con pytest contra las cifras de control y casos límite de AGENTS.md, más `VALIDACION.md` con esperado vs obtenido | `tests/test_*.py`, `VALIDACION.md` | Todas las entregas de backend y frontend | Ejecutar `pytest` y ver que todas las pruebas pasan; leer `VALIDACION.md` |
| 10 | @revisor | Revisión de seguridad (llaves, `.env`, datos sensibles, `.gitignore`) y cumplimiento de AGENTS.md, con lista de hallazgos por prioridad y corrección propuesta | `REVISION.md` (o similar, solo reporte) | Todas las entregas anteriores | Leer el reporte de hallazgos en pantalla |

## 4. PUNTOS DE CONTROL

| Después de la entrega | Quiere intervenir | Qué debe ver el usuario en pantalla exactamente |
|---|---|---|
| 2 (estructura MVC) | @tester (opcional, solo humo) | `iniciar_app.bat` abre el navegador y la app Flask responde (pantalla de inicio o 404 de rutas) |
| 6 (agente de IA) | @tester | JSON válido en pantalla con todos los campos: `numero_cartel`, `institucion_emisora`, `presupuesto_estimado`, `moneda`, `fecha_limite_presentacion`, `resumen_alcance`, `requisitos_experiencia`, `viabilidad_participacion`, `justificacion_viabilidad` |
| 8 (pantallas) | @tester | Pantalla de resultados con contadores grandes visibles, tabla con filtro funcional, y detalle por registro al hacer clic |
| 9 (pruebas) | @revisor | `pytest` ejecutado y todas las pruebas pasan; `VALIDACION.md` muestra esperado vs obtenido sin diferencias no justificadas |
| 10 (revisión) | Usuario | `REVISION.md` con lista de hallazgos (prioridad alta/media/baja), ubicación y corrección propuesta; sin llaves en código ni `.env` subido a GitHub |

## 5. RIESGOS

| Riesgo | Qué hará cada subagente si pasa |
|---|---|
| Datos incompletos (falta `.env`, falta carteles de SICOP) | @backend: no inventa llaves ni columnas; pregunta al usuario antes de continuar. @arquitecto: registra el faltante en PLAN.md y pausa la entrega afectada. |
| Archivos escaneados (PDF imagen sin texto) | @backend: detecta que no hay texto extraíble y avisa que se requiere OCR (caso límite de AGENTS.md). @tester: incluye prueba de caso límite con PDF escaneado. |
| Respuesta del agente que no es JSON válido | @backend: valida la salida del agente antes de usarla; si no es JSON, devuelve error controlado y avisa. @tester: prueba con respuesta malformada. |
| Llave gratis de IA agotada o con límites | @backend: lee la llave de `.env`; si falla por cuota, informa el error sin hardcodear alternativas. @revisor: verifica que no haya llaves escritas en el código. |
| Insumos modificados o con adendas de última hora | @tester: incluye caso límite de reevalución de análisis previo. @arquitecto: actualiza PLAN.md si cambia el alcance. |

## 6. PREGUNTAS PARA MÍ
Antes de que @backend comience la entrega 2, necesito confirmar:

1. ¿La app debe realmente conectarse y descargar del portal SICOP en vivo, o solo simular la descarga con los PDFs de `insumos` como entrada de prueba?
2. ¿Tengo permiso para crear un archivo `.env` con una llave de prueba, o debo dejar solo `.env.example` y que usted llene la llave real?
3. ¿El "documento de entendimiento del TDR" que produce la app es un archivo (PDF/Word/Markdown) generado por la app, o solo se muestra en pantalla?
4. ¿Las alertas/notificaciones automáticas se envían por correo, se guardan en un archivo, o solo se muestran en la interfaz web?

---

**Esperando su aprobación del PLAN.md antes de que comience cualquier subagente.**
