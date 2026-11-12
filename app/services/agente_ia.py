"""Integración del agente de IA.

Lee la llave de API desde .env, llama al agente y devuelve el contrato JSON
estructurado con los campos definidos en AGENTS.md.
"""

import os


def _cargar_env(ruta_env=".env"):
    """Carga variables de entorno desde un archivo .env (Python puro, sin librerías externas)."""
    if not os.path.exists(ruta_env):
        return
    with open(ruta_env, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                os.environ.setdefault(clave.strip(), valor.strip())


# Cargar variables de .env al importar este módulo
_cargar_env()


def analizar_con_agente_ia(texto_cartel: str, numero_cartel: str = "N/A") -> dict:
    """Analiza un cartel mediante el agente de IA y retorna el contrato JSON.

    Lee la llave de API de IA_API_KEY en .env. Si no está configurada,
    retorna un error controlado sin hardcodear claves.
    """
    api_key = os.getenv("IA_API_KEY")

    if not api_key or api_key == "tu_llave_de_api_aqui":
        return {
            "error": "IA_API_KEY no configurada en .env",
            "numero_cartel": numero_cartel,
            "estado": "pendiente_configuracion_llave",
        }

    # TODO: Llamar al agente de IA real con la llave configurada.
    # Aquí se enviaría texto_cartel al modelo y se parsearía la respuesta JSON.
    # Por ahora se retorna un contrato JSON de ejemplo basado en AGENTS.md.
    contrato_json = {
        "numero_cartel": numero_cartel,
        "institucion_emisora": "Institución detectada en el cartel",
        "presupuesto_estimado": 50000000,
        "moneda": "CRC",
        "fecha_limite_presentacion": "2026-12-31T16:00:00",
        "resumen_alcance": "Análisis de alcance del TDR pendiente de confirmación con el agente de IA",
        "requisitos_experiencia": {
            "personal": "Certificación requerida (pendiente del agente de IA)",
            "fabricante": "Partner Premier (pendiente del agente de IA)",
        },
        "viabilidad_participacion": "Media",
        "justificacion_viabilidad": "Perfil técnico pendiente de validación por el agente de IA",
        "origen": "contrato_json_simulado",
    }

    return contrato_json
