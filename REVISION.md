# REVISION.md - Informe de revisión de seguridad y cumplimiento AGENTS.md

Fecha: 2026-11-04
Proyecto: Analisis carteles SICOP - Preventa Comercial TI
Revisor: @revisor (modo: solo lectura, sin modificaciones)

## Resumen

| Prioridad | Cantidad |
|---|---|
| Alta | 1 |
| Media | 3 |
| Baja | 2 |
| Total | 6 |

## Hallazgos

### [ALTA] Archivo .env con llave de API incluida en el repositorio

**Descripción:** El archivo `.env` fue creado con un valor placeholder `IA_API_KEY=tu_llave_de_api_aqui`. Aunque es un placeholder, el archivo `.env` contiene credenciales y no debería subirse a GitHub.

**Ubicación:** `C:\Users\Stwart\OneDrive\Desktop\Proyectos Módulo II\Analisis carteles\.env`

**Corrección propuesta:** El archivo `.env` ya está incluido en `.gitignore`. Verificar que `.gitignore` esté activo y que `.env` nunca se agregue al control de versiones. Mantener solo `.env.example` en el repositorio.

---

### [MEDIA] Llave de API hardcodeada en pruebas (tests/test_app.py)

**Descripción:** Las pruebas asignan `os.environ["IA_API_KEY"] = "sk-test-1234567890"` directamente en el código de prueba. Aunque es una llave de prueba simulada, es una práctica que debería evitarse en código fuente.

**Ubicación:** `tests/test_app.py` (líneas con `os.environ["IA_API_KEY"] = "sk-test-1234567890"`)

**Corrección propuesta:** Usar una variable de entorno real en el entorno de ejecución, no hardcodear en las pruebas. O usar `monkeypatch` de pytest para establecer la variable temporalmente durante la prueba.

---

### [MEDIA] Carpeta repositorio_central creada durante pruebas de regla R3

**Descripción:** La función `clasificar_y_enrutar_documento` crea carpetas físicas en `repositorio_central/` durante la ejecución. Esto genera archivos no deseados en el directorio del proyecto.

**Ubicación:** `repositorio_central/` (creado durante pruebas)

**Corrección propuesta:** Agregar `repositorio_central/` a `.gitignore` para evitar que se suba a GitHub. En producción, esta carpeta debería estar fuera del código fuente o configurada como variable de entorno.

---

### [MEDIA] Carpeta .pytest_cache generada por pytest

**Descripción:** Pytest genera la carpeta `.pytest_cache/` en la raíz del proyecto.

**Ubicación:** `.pytest_cache/`

**Corrección propuesta:** Agregar `.pytest_cache/` a `.gitignore`.

---

### [BAJA] Archivo de prueba temporal test_r3_temp.py eliminado

**Descripción:** Se verificó que el archivo temporal `test_r3_temp.py` fue eliminado correctamente después de su uso. No queda rastro en el proyecto.

**Estado:** ✅ Resuelto (archivo eliminado)

---

### [BAJA] Falta de rutas de controlador separadas (todo en app/__init__.py)

**Descripción:** Las rutas de Flask están definidas directamente en `app/__init__.py` en lugar de usar blueprints en `app/controllers/`. Esto no viola AGENTS.md pero no sigue estrictamente el patrón MVC descrito en el plan.

**Ubicación:** `app/__init__.py`

**Corrección propuesta:** Mover las rutas a `app/controllers/` usando blueprints de Flask cuando se escalen los controladores. Actualmente funciona correctamente con las rutas en `__init__.py`.

---

## Cumplimiento con AGENTS.md

| Requisito de AGENTS.md | Estado | Observación |
|---|---|---|
| Separación de responsabilidades | ✅ Cumplido | Reglas deterministas en `app/services/`, agente de IA separado |
| Trazabilidad | ✅ Cumplido | Cada función tiene su comentario y origen documentado |
| Seguridad y cumplimiento | ⚠️ Parcial | `.env` en `.gitignore`, pero llave de prueba hardcodeada en tests |
| No modificar insumos/contexto | ✅ Cumplido | Ningún archivo de `insumos/` o `contexto/` fue modificado |
| No inventar columnas ni reglas | ✅ Cumplido | Toda lógica basada en AGENTS.md |
| Contrato JSON del agente | ✅ Cumplido | Todos los 9 campos del contrato presentes |
| Datos de entrada = PDF de SICOP | ✅ Cumplido | Los PDFs de `insumos/` son referencia normativa, no entrada |

## Conclusión

El proyecto cumple con AGENTS.md en lo esencial. El único hallazgo de prioridad alta es la presencia del archivo `.env` en el repositorio (aunque ya está en `.gitignore`). Se recomienda corregir los hallazgos de media prioridad antes de llevar el código a producción.

**Verificación en pantalla:** Este reporte se genera como archivo `REVISION.md` (guardado como `REVISION.md` en la raíz del proyecto). Todos los hallazgos fueron revisados leyendo el código sin modificarlo.
