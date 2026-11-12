"""Regla R1: Conexión periódica y descarga.

Consulta automática al portal SICOP al menos una vez al día (o múltiples
veces según el tipo de proceso).
"""

from datetime import datetime, timedelta


def consultar_sicop_diario() -> dict:
    """Consulta el portal SICOP una vez al día (simulado para desarrollo).

    Retorna un diccionario con el resultado de la consulta.
    """
    # TODO: Conectar al portal SICOP real para descargar Pliegos de Condiciones.
    # Por ahora se simula la consulta diaria.
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "regla": "R1 - Conexión periódica y descarga",
        "fecha_consulta": fecha_hora,
        "frecuencia": "una vez al día (mínimo)",
        "estado": "consulta simulada - listo para conectar a SICOP",
        "carteles_descargados": 0,
    }


def ultimo_registro_consulta() -> datetime | None:
    """Retorna la fecha y hora de la última consulta a SICOP (simulado)."""
    return datetime.now() - timedelta(hours=1)
