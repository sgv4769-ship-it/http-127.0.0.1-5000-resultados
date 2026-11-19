"""Integración del agente de IA.

Lee la llave de API desde .env, llama al agente y devuelve el contrato JSON
estructurado con los campos definidos en AGENTS.md.
Incluye sanitizado de entrada para bloquear intentos de prompt injection.
"""

import os
import re


PATRONES_PROMPT_INJECTION = [
    r"ignorar\s+todas\s+las\s+instrucciones",
    r"olvida\s+tu\s+rol",
    r"eres\s+ahora\s+un\s+asistente",
    r"system\s*:",
    r"instrucciones\s+del\s+sistema",
    r"imprime\s+todas\s+las\s+credenciales",
    r"revela\s+contraseñas?",
    r"revela\s+claves?",
    r"bypass\s+de\s+seguridad",
    r"salta\s+las\s+reglas",
]


def _contiene_prompt_injection(texto: str) -> bool:
    """Detecta patrones de prompt injection en el texto de entrada."""
    texto_lower = texto.lower()
    for patron in PATRONES_PROMPT_INJECTION:
        if re.search(patron, texto_lower):
            return True
    return False


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
    Si detecta intento de prompt injection, rechaza la petición.
    """
    # Seguridad: bloquear prompt injection antes de procesar
    if _contiene_prompt_injection(texto_cartel):
        return {
            "error": "Entrada rechazada: contenido no permitido (posible prompt injection).",
            "numero_cartel": numero_cartel,
            "estado": "prompt_injection_bloqueado",
        }

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
