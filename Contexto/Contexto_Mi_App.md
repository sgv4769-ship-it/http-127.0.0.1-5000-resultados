# Contexto - Mi App

## 1. Qué es esta app
Es una solución de automatización e inteligencia artificial diseñada para el área de TI – Preventa Comercial. Su propósito es conectarse periódicamente al portal de compras públicas de Costa Rica (SICOP) para descargar, leer y analizar los Pliegos de Condiciones (TDR / Carteles) y documentos anexos, evaluando la viabilidad técnica y comercial de participar en cada concurso público.

## 2. Reglas de negocio (código)
Las reglas deterministas ejecutadas mediante código o herramientas de automatización (como n8n o Power Automate) incluyen:

- **Conexión periódica y descarga:** Consulta automática al portal SICOP al menos una vez al día (o múltiples veces según el tipo de proceso).
- **Filtros duros iniciales:** Validación de criterios objetivos como rangos de presupuesto, plazos de entrega, tipo de industria o líneas de negocio de TI afines antes de pasar al análisis profundo.
- **Inventario y enrutamiento:** Clasificación de los documentos descargados (diagramas, estudios de mercado, anexos) y organización en un repositorio central.

## 3. Lo que hace el agente de IA y su contrato JSON

**Lo que hace el agente:**
Realiza una lectura comprensiva y analítica de los textos complejos y extensos de los carteles (que normalmente toman entre 2 y 5 horas por documento). Interpreta el contexto técnico-comercial, resume los requerimientos y emite una recomendación preliminar de viabilidad.

**Contrato JSON estructurado (ejemplo de salida):**
```json
{
  "numero_cartel": "2026XE-0000XX-000100001",
  "institucion_emisora": "Nombre de la Institución",
  "presupuesto_estimado": 50000000,
  "moneda": "CRC",
  "fecha_limite_presentacion": "2026-12-31T16:00:00",
  "resumen_alcance": "Migración de servidores de respaldo...",
  "requisitos_experiencia": {
    "personal": "Certificación requerida...",
    "fabricante": "Partner Premier..."
  },
  "viabilidad_participacion": "Alta / Media / Baja",
  "justificacion_viabilidad": "El perfil técnico coincide con las verticales de negocio actuales."
}
```

## 4. Qué produce la app
- Un documento de entendimiento del TDR que sintetiza los requerimientos, productos, alcances, especificaciones de entrega (experiencia personal y de fabricante), presupuesto estimado y la viabilidad de participar.
- Alertas y notificaciones automáticas para involucrar de manera temprana a las respectivas verticales de negocio y equipos de desarrollo internos.

## 5. Quién decide
El equipo humano de preventa comercial (en este caso, los profesionales responsables del proceso). La IA actúa como un asistente analítico avanzado que acelera la revisión y filtra la información, pero la decisión final de participar o no en el concurso recae 100% sobre los expertos comerciales y técnicos.

## 6. Cifras de control
- **Tiempo de lectura por cartel:** Reducción drástica del tiempo actual (que oscila entre 2 y 5 horas por documento) a cuestión de minutos mediante el análisis automatizado.
- **Frecuencia de ejecución:** Número de revisiones diarias en SICOP (mínimo una vez al día o múltiples veces según la demanda de procesos).
- **Tasa de conversión de viabilidad:** Porcentaje de carteles analizados que resultan ser viables frente a los descartados.
- **Precisión en la extracción:** Porcentaje de campos clave correctamente identificados en el contrato JSON frente al documento original del TDR.

## 7. Casos límite (Edge Cases)
- **Documentos no estructurados o escaneados:** Carteles o estudios de mercado presentados en formato PDF imagen que requieren capacidades avanzadas de OCR antes de ser procesados por el agente.
- **Aclaraciones y modificaciones de última hora:** Carteles en SICOP que sufren modificaciones o adendas posteriores a su publicación inicial, lo que requiere reevaluar el análisis previo.
- **Presupuestos o requerimientos ambiguos:** Concursos donde la información económica o las especificaciones técnicas del fabricante no están claramente detalladas, generando dudas en la viabilidad.

## 8. Reglas del sistema
- **Separación de responsabilidades:** Separar estrictamente las tareas deterministas (descarga de archivos, filtros lógicos por código) de las tareas cognitivas e interpretativas (análisis del contenido del cartel a cargo del agente de IA).
- **Trazabilidad:** Cada recomendación del agente debe estar respaldada y vinculada directamente con las secciones del documento fuente descargado de SICOP para facilitar la auditoría humana.
- **Seguridad y cumplimiento:** Manejo adecuado de la información pública institucional bajo los estándares operativos definidos para el análisis de preventa comercial.
