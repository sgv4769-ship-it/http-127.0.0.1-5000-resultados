"""Regla R3: Inventario y enrutamiento.

Clasificación de los documentos descargados (diagramas, estudios de mercado,
anexos) y organización en un repositorio central.
"""

import os
from pathlib import Path


REPOSITORIO_CENTRAL = Path("repositorio_central")


def clasificar_y_enrutar_documento(ruta_archivo: str) -> dict:
    """Clasifica un documento descargado y lo enruta al repositorio central.

    Recibe la ruta del archivo y determina su tipo (diagrama, estudio de
    mercado, anexo, pliego) para organizar en el repositorio.
    """
    archivo = Path(ruta_archivo)
    nombre = archivo.name.lower()
    extension = archivo.suffix.lower()

    # Clasificación por nombre y extensión
    if "anexo" in nombre:
        tipo = "anexo"
        carpeta_destino = REPOSITORIO_CENTRAL / "anexos"
    elif "estudio" in nombre or "mercado" in nombre:
        tipo = "estudio_mercado"
        carpeta_destino = REPOSITORIO_CENTRAL / "estudios_mercado"
    elif "diagrama" in nombre:
        tipo = "diagrama"
        carpeta_destino = REPOSITORIO_CENTRAL / "diagramas"
    elif "pliego" in nombre or "cartel" in nombre or extension == ".pdf":
        tipo = "pliego_cartel"
        carpeta_destino = REPOSITORIO_CENTRAL / "pliegos_carteles"
    else:
        tipo = "documento_general"
        carpeta_destino = REPOSITORIO_CENTRAL / "documentos_generales"

    # Crear carpeta de destino si no existe
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    return {
        "regla": "R3 - Inventario y enrutamiento",
        "archivo_origen": str(archivo),
        "tipo_clasificado": tipo,
        "carpeta_destino": str(carpeta_destino),
        "extension": extension,
        "enrutado": True,
    }
