"""Generador de documento de entendimiento del TDR.

Produce un documento de entendimiento del TDR que sintetiza los requerimientos,
productos, alcances, especificaciones de entrega (experiencia personal y de
fabricante), presupuesto estimado y la viabilidad de participar.
Según AGENTS.md, sección "Qué produce la app".
"""

from datetime import datetime


def generar_documento_tdr(contrato_json: dict, ruta_origen: str = "") -> str:
    """Genera el documento de entendimiento del TDR en formato Markdown.

    Recibe el contrato JSON del agente de IA y devuelve el contenido del
    documento listo para guardarse como archivo.
    """
    viabilidad = contrato_json.get("viabilidad_participacion", "No definida")
    justificacion = contrato_json.get("justificacion_viabilidad", "")
    presupuesto = contrato_json.get("presupuesto_estimado", 0)
    moneda = contrato_json.get("moneda", "CRC")
    fecha_limite = contrato_json.get("fecha_limite_presentacion", "")
    resumen = contrato_json.get("resumen_alcance", "")
    institucion = contrato_json.get("institucion_emisora", "")
    numero_cartel = contrato_json.get("numero_cartel", "")
    requisitos = contrato_json.get("requisitos_experiencia", {})
    personal = requisitos.get("personal", "")
    fabricante = requisitos.get("fabricante", "")

    fecha_analisis = datetime.now().strftime("%d/%m/%Y %H:%M")

    documento = f"""# DOCUMENTO DE ENTENDIMIENTO DEL TDR

## Información General
- **Número de cartel:** {numero_cartel}
- **Institución emisora:** {institucion}
- **Fecha de análisis:** {fecha_analisis}
- **Documento fuente:** {ruta_origen or "No especificado"}

## Presupuesto y Plazos
- **Presupuesto estimado:** {presupuesto:,.0f} {moneda}
- **Fecha límite de presentación:** {fecha_limite}

## Alcance del Proyecto
{resumen}

## Requisitos de Experiencia
### Personal
{personal}

### Fabricante
{fabricante}

## Viabilidad de Participación
- **Viabilidad:** {viabilidad}
- **Justificación:** {justificacion}

---
*Documento generado automáticamente por el sistema de análisis de carteles SICOP.*
*La decisión final de participar recae 100% sobre el equipo humano de preventa comercial.*
"""
    return documento


def guardar_documento_tdr(contenido: str, ruta_salida: str) -> bool:
    """Guarda el documento de entendimiento en un archivo."""
    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except Exception:
        return False
