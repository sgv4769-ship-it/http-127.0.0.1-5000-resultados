# AGENTS.md

## Qué es esta app
Solución de automatización e inteligencia artificial para el área de TI – Preventa Comercial. Se conecta periódicamente al portal de compras públicas de Costa Rica (SICOP) para descargar, leer y analizar los Pliegos de Condiciones (TDR / Carteles) y documentos anexos, evaluando la viabilidad técnica y comercial de participar en cada concurso público.

## Datos de entrada
Los datos de entrada son **PDF descargados del portal SICOP** (Pliegos de Condiciones / TDR / Carteles y documentos anexos). No hay archivos Excel ni CSV con columnas y filas.

Los archivos de la carpeta `insumos` se tratan como **referencia normativa** (no son datos de entrada):

| Archivo (insumos) | Páginas | Texto | De qué trata |
|---|---|---|---|
| `Ley_N__9986_Reglamento_Ley_General_de_Contratación_Pública.pdf` | 190 | 190/190 con texto | Reglamento de la Ley General de Contratación Pública (Ley 9986), Costa Rica. Artículos 1 al 328. Referencia normativa. |
| `Pliego de condiciones - Adquisición de un WAF (2).pdf` | 19 | 19/19 con texto | Licitación reducida del BANHVI para adquirir un Web Application Firewall (WAF) Administrado. Condiciones generales, presentación de ofertas por SICOP, criterios de evaluación, adjudicación, rifa en caso de empate. Ejemplo de pliego/cartel. |
| `ley-general-contratacion-publica-9986.pdf` | 97 | 97/97 con texto | Ley General de Contratación Pública No. 9986 (Decreto Legislativo, expediente 21.546). Disposiciones generales, principios, procedimientos de contratación. Referencia normativa. |

## Reglas de negocio (código)
Las reglas deterministas ejecutadas mediante código o herramientas de automatización (como n8n o Power Automate) incluyen:

- **Conexión periódica y descarga:** consulta automática al portal SICOP al menos una vez al día (o múltiples veces según el tipo de proceso).
- **Filtros duros iniciales:** validación de criterios objetivos como rangos de presupuesto, plazos de entrega, tipo de industria o líneas de negocio de TI afines antes de pasar al análisis profundo.
- **Inventario y enrutamiento:** clasificación de los documentos descargados (diagramas, estudios de mercado, anexos) y organización en un repositorio central.

## Lo que hace el agente de IA (contrato JSON)
El agente realiza una lectura comprensiva y analítica de los textos complejos y extensos de los carteles (que normalmente toman entre 2 y 5 horas por documento). Interpreta el contexto técnico-comercial, resume los requerimientos y emite una recomendación preliminar de viabilidad.

**Contrato JSON estructurado (salida del agente):**
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

## Qué produce la app
- Un documento de entendimiento del TDR que sintetiza los requerimientos, productos, alcances, especificaciones de entrega (experiencia personal y de fabricante), presupuesto estimado y la viabilidad de participar.
- Alertas y notificaciones automáticas para involucrar de manera temprana a las respectivas verticales de negocio y equipos de desarrollo internos.

## Quién decide
El equipo humano de preventa comercial (profesionales responsables del proceso). La IA actúa como un asistente analítico avanzado que acelera la revisión y filtra la información, pero la decisión final de participar o no en el concurso recae **100%** sobre los expertos comerciales y técnicos.

## Cifras de control
- **Tiempo de lectura por cartel:** reducción de 2–5 horas por documento a cuestión de minutos mediante el análisis automatizado.
- **Frecuencia de ejecución:** número de revisiones diarias en SICOP (mínimo una vez al día o múltiples veces según la demanda de procesos).
- **Tasa de conversión de viabilidad:** porcentaje de carteles analizados que resultan viables frente a los descartados.
- **Precisión en la extracción:** porcentaje de campos clave correctamente identificados en el contrato JSON frente al documento original del TDR.

## Casos límite (Edge Cases)
- **Documentos no estructurados o escaneados:** carteles o estudios de mercado en formato PDF imagen que requieren capacidades avanzadas de OCR antes de ser procesados por el agente.
- **Aclaraciones y modificaciones de última hora:** carteles en SICOP que sufren modificaciones o adendas posteriores a su publicación inicial, lo que requiere reevaluar el análisis previo.
- **Presupuestos o requerimientos ambiguos:** concursos donde la información económica o las especificaciones técnicas del fabricante no están claramente detalladas, generando dudas en la viabilidad.

## Reglas del sistema
- **Separación de responsabilidades:** separar estrictamente las tareas deterministas (descarga de archivos, filtros lógicos por código) de las tareas cognitivas e interpretativas (análisis del contenido del cartel a cargo del agente de IA).
- **Trazabilidad:** cada recomendación del agente debe estar respaldada y vinculada directamente con las secciones del documento fuente descargado de SICOP para facilitar la auditoría humana.
- **Seguridad y cumplimiento:** manejo adecuado de la información pública institucional bajo los estándares operativos definidos para el análisis de preventa comercial.


