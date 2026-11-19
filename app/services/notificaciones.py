"""Módulo de notificaciones y alertas automáticas.

Envía alertas para involucrar de manera temprana a las respectivas
verticales de negocio y equipos de desarrollo internos.
Según AGENTS.md, sección "Qué produce la app".
"""

from datetime import datetime


def generar_alerta_viabilidad(contrato_json: dict, destino_vertical: str = "TI") -> dict:
    """Genera una alerta de viabilidad para notificar a la vertical de negocio.

    Retorna un diccionario con los datos de la alerta listos para enviarse
    por correo, guardarse en archivo o mostrar en la interfaz.
    """
    viabilidad = contrato_json.get("viabilidad_participacion", "No definida")
    numero_cartel = contrato_json.get("numero_cartel", "N/A")
    institucion = contrato_json.get("institucion_emisora", "No especificada")
    presupuesto = contrato_json.get("presupuesto_estimado", 0)
    moneda = contrato_json.get("moneda", "CRC")
    fecha_limite = contrato_json.get("fecha_limite_presentacion", "")
    justificacion = contrato_json.get("justificacion_viabilidad", "")

    fecha_alerta = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Determinar prioridad según viabilidad
    if viabilidad == "Alta":
        prioridad = "ALTA"
        asunto = f"[ALTA] Cartel viable: {numero_cartel} - {institucion}"
    elif viabilidad == "Media":
        prioridad = "MEDIA"
        asunto = f"[MEDIA] Revisar cartel: {numero_cartel} - {institucion}"
    else:
        prioridad = "BAJA"
        asunto = f"[BAJA] Cartel descartado: {numero_cartel} - {institucion}"

    mensaje = f"""
Nuevo cartel analizado por el sistema SICOP.

Número: {numero_cartel}
Institución: {institucion}
Presupuesto: {presupuesto:,.0f} {moneda}
Fecha límite: {fecha_limite}
Viabilidad: {viabilidad}
Justificación: {justificacion}

Vertical destino: {destino_vertical}
Fecha de alerta: {fecha_alerta}

La decisión final de participar recae 100% sobre el equipo humano de preventa.
"""

    return {
        "asunto": asunto,
        "mensaje": mensaje,
        "prioridad": prioridad,
        "viabilidad": viabilidad,
        "numero_cartel": numero_cartel,
        "destino_vertical": destino_vertical,
        "fecha_alerta": fecha_alerta,
    }


def formatear_alerta_para_correo(alerta: dict) -> str:
    """Formatea la alerta como cuerpo de correo electrónico."""
    return f"""
Asunto: {alerta['asunto']}

Estimado equipo de {alerta['destino_vertical']},

{alerta['mensaje']}

---
Sistema de Análisis de Carteles SICOP - Preventa Comercial TI
"""


def guardar_alerta_en_archivo(alerta: dict, ruta_salida: str) -> bool:
    """Guarda la alerta en un archivo de texto."""
    try:
        contenido = formatear_alerta_para_correo(alerta)
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except Exception:
        return False
