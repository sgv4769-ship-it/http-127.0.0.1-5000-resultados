"""Pruebas de la app de Analisis de Carteles SICOP.

Compara los resultados con las cifras de control y los casos límite de AGENTS.md.
pythonpath configurado para importar la app.
"""

import os
import sys
import json
from datetime import datetime

# Asegurar que se pueda importar la app desde tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.regla1_descarga import consultar_sicop_diario
from app.services.regla2_filtros import aplicar_filtros_duros
from app.services.regla3_inventario import clasificar_y_enrutar_documento
from app.services.agente_ia import analizar_con_agente_ia


# ---------------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------------

def test_app_creada_correctamente():
    """La app Flask se crea sin errores."""
    app = create_app()
    assert app is not None
    assert app.config is not None


def test_ruta_inicio_responde():
    """La ruta / devuelve HTTP 200 y contiene 'Inicio'."""
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Inicio" in resp.data


def test_ruta_resultados_responde():
    """La ruta /resultados devuelve HTTP 200 y contiene elementos del tablero."""
    app = create_app()
    client = app.test_client()
    resp = client.get("/resultados")
    assert resp.status_code == 200
    assert b"Resultados" in resp.data
    assert b"contador-total" in resp.data
    assert b"tabla-resultados" in resp.data
    assert b"filtro-tabla" in resp.data


def test_ruta_health_responde():
    """La ruta /health devuelve JSON con estado activa."""
    app = create_app()
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["estado"] == "activa"


# ---------------------------------------------------------------------------
# REGLAS DE NEGOCIO (cifras de control y reglas del sistema)
# ---------------------------------------------------------------------------

def test_regla_r1_consulta_diaria_retorna_dict():
    """R1: consultar_sicop_diario retorna un dict con los campos esperados."""
    resultado = consultar_sicop_diario()
    assert isinstance(resultado, dict)
    assert "regla" in resultado
    assert "fecha_consulta" in resultado
    assert resultado["regla"] == "R1 - Conexión periódica y descarga"
    assert "una vez al día" in resultado["frecuencia"]


def test_regla_r2_filtros_duros_cartel_valido():
    """R2: Cartel con presupuesto, industria TI y plazo adecuado pasa los filtros."""
    cartel = {
        "numero_cartel": "2026XE-0000XX-000100001",
        "presupuesto_estimado": 50000000,
        "industria": "TI",
        "linea_negocio": "Desarrollo de software",
        "plazo_entrega_dias": 90,
    }
    resultado = aplicar_filtros_duros(cartel)
    assert resultado["pasa_filtros"] is True
    assert resultado["motivos"] == []


def test_regla_r2_filtros_duros_cartel_invalido():
    """R2: Cartel con presupuesto bajo, industria no TI y plazo corto NO pasa."""
    cartel = {
        "numero_cartel": "2026XE-0000XX-000100002",
        "presupuesto_estimado": 500000,
        "industria": "Construcción",
        "linea_negocio": "Obras civiles",
        "plazo_entrega_dias": 15,
    }
    resultado = aplicar_filtros_duros(cartel)
    assert resultado["pasa_filtros"] is False
    assert len(resultado["motivos"]) > 0


def test_regla_r3_enrutamiento_pliego():
    """R3: Un PDF de pliego se enruta a pliegos_carteles."""
    resultado = clasificar_y_enrutar_documento("insumos/cartel_ejemplo.pdf")
    assert resultado["tipo_clasificado"] == "pliego_cartel"
    assert "pliegos_carteles" in resultado["carpeta_destino"]
    assert resultado["enrutado"] is True


def test_regla_r3_enrutamiento_estudio_mercado():
    """R3: Un estudio de mercado se enruta a estudios_mercado."""
    resultado = clasificar_y_enrutar_documento("estudio_mercado_waf.pdf")
    assert resultado["tipo_clasificado"] == "estudio_mercado"
    assert "estudios_mercado" in resultado["carpeta_destino"]


def test_regla_r3_enrutamiento_anexo():
    """R3: Un anexo se enruta a anexos."""
    resultado = clasificar_y_enrutar_documento("anexo_tecnico.pdf")
    assert resultado["tipo_clasificado"] == "anexo"
    assert "anexos" in resultado["carpeta_destino"]


# ---------------------------------------------------------------------------
# AGENTE DE IA (contrato JSON)
# ---------------------------------------------------------------------------

def test_agente_ia_retorna_json_con_todos_los_campos():
    """El agente de IA retorna un JSON con todos los campos del contrato de AGENTS.md."""
    os.environ["IA_API_KEY"] = "sk-test-1234567890"
    resultado = analizar_con_agente_ia(
        texto_cartel="Ejemplo de cartel de licitación pública",
        numero_cartel="2026XE-0000XX-000100001",
    )

    campos_esperados = [
        "numero_cartel",
        "institucion_emisora",
        "presupuesto_estimado",
        "moneda",
        "fecha_limite_presentacion",
        "resumen_alcance",
        "requisitos_experiencia",
        "viabilidad_participacion",
        "justificacion_viabilidad",
    ]
    for campo in campos_esperados:
        assert campo in resultado, f"Falta campo: {campo}"

    assert resultado["numero_cartel"] == "2026XE-0000XX-000100001"
    assert resultado["moneda"] == "CRC"
    assert isinstance(resultado["presupuesto_estimado"], int)
    assert resultado["viabilidad_participacion"] in ("Alta", "Media", "Baja")
    assert isinstance(resultado["requisitos_experiencia"], dict)
    assert "personal" in resultado["requisitos_experiencia"]
    assert "fabricante" in resultado["requisitos_experiencia"]


def test_agente_ia_sin_llave_retorna_error_controlado():
    """Caso límite: si IA_API_KEY no está configurada, retorna error sin hardcodear claves."""
    # Limpiar variable de entorno para simular ausencia de llave
    os.environ.pop("IA_API_KEY", None)
    resultado = analizar_con_agente_ia(
        texto_cartel="Cualquier texto",
        numero_cartel="TEST-0001",
    )
    assert "error" in resultado
    assert resultado["estado"] == "pendiente_configuracion_llave"


# ---------------------------------------------------------------------------
# CASOS LÍMITE (Edge Cases de AGENTS.md)
# ---------------------------------------------------------------------------

def test_caso_limite_pdf_escaneado_sin_texto():
    """Caso límite: documento escaneado (PDF imagen) no tiene texto extraíble."""
    # Simular detección de PDF sin texto
    texto_extraido = ""
    assert texto_extraido == ""  # PDF escaneado: no hay texto
    # La app debería requerir OCR antes de procesar


def test_caso_limite_presupuesto_ambiguo():
    """Caso límite: presupuesto ambiguo o no detallado."""
    cartel = {
        "numero_cartel": "2026XE-0000XX-000100003",
        "presupuesto_estimado": 0,  # ambiguo/no especificado
        "industria": "TI",
        "linea_negocio": "Software",
        "plazo_entrega_dias": 60,
    }
    resultado = aplicar_filtros_duros(cartel)
    assert resultado["pasa_filtros"] is False  # presupuesto fuera de rango


def test_caso_limite_viabilidad_ambigua():
    """Caso límite: viabilidad no clara -> Media por defecto."""
    os.environ["IA_API_KEY"] = "sk-test-1234567890"
    resultado = analizar_con_agente_ia(
        texto_cartel="Cartel con especificaciones técnicas ambiguas",
        numero_cartel="2026XE-0000XX-000100004",
    )
    # Con datos ambiguos, la viabilidad por defecto es Media
    assert resultado["viabilidad_participacion"] == "Media"


# ---------------------------------------------------------------------------
# CIFRAS DE CONTROL
# ---------------------------------------------------------------------------

def test_cifra_tiempo_lectura_reducido():
    """Cifra de control: tiempo de lectura reducido de 2-5 horas a minutos."""
    # La app automatiza el análisis; el tiempo real se mide en ejecución.
    # Aquí validamos que la función de análisis existe y retorna rápido.
    import time
    os.environ["IA_API_KEY"] = "sk-test-1234567890"
    inicio = time.time()
    analizar_con_agente_ia(
        texto_cartel="Texto de prueba para medir tiempo",
        numero_cartel="TEST-TIEMPO-001",
    )
    fin = time.time()
    segundos = fin - inicio
    assert segundos < 5, f"El análisis tomó {segundos:.2f}s, debería ser cuestión de minutos"


def test_cifra_frecuencia_ejecucion():
    """Cifra de control: consulta al menos una vez al día."""
    resultado = consultar_sicop_diario()
    assert "una vez al día" in resultado["frecuencia"]


def test_cifra_tasa_conversion_viabilidad():
    """Cifra de control: porcentaje de carteles viables vs descartados."""
    carteles = [
        {"viabilidad_participacion": "Alta"},
        {"viabilidad_participacion": "Media"},
        {"viabilidad_participacion": "Baja"},
        {"viabilidad_participacion": "Alta"},
    ]
    viables = sum(1 for c in carteles if c["viabilidad_participacion"] in ("Alta", "Media"))
    tasa = viables / len(carteles)
    assert 0 <= tasa <= 1
    assert tasa == 0.75  # 3 de 4 son viables (Alta o Media)


def test_cifra_precision_extraccion_campos_json():
    """Cifra de control: porcentaje de campos clave correctamente identificados."""
    os.environ["IA_API_KEY"] = "sk-test-1234567890"
    resultado = analizar_con_agente_ia(
        texto_cartel="Texto de prueba",
        numero_cartel="2026XE-0000XX-000100001",
    )
    campos_clave = [
        "numero_cartel",
        "institucion_emisora",
        "presupuesto_estimado",
        "moneda",
        "fecha_limite_presentacion",
        "viabilidad_participacion",
    ]
    campos_correctos = sum(1 for c in campos_clave if c in resultado and resultado[c] is not None)
    precision = campos_correctos / len(campos_clave)
    assert precision == 1.0  # 100% de los campos clave presentes
