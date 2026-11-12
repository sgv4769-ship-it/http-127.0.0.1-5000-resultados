"""Regla R2: Filtros duros iniciales.

Validación de criterios objetivos como rangos de presupuesto, plazos de
entrega, tipo de industria o líneas de negocio de TI afines antes de pasar al
análisis profundo.
"""


def aplicar_filtros_duros(cartel: dict) -> dict:
    """Valida criterios objetivos de un cartel antes del análisis profundo.

    Recibe un diccionario con campos del cartel y retorna si pasa o no los
    filtros duros, con el motivo.
    """
    presupuesto = cartel.get("presupuesto_estimado", 0)
    industria = cartel.get("industria", "")
    linea_negocio = cartel.get("linea_negocio", "")
    plazo_entrega = cartel.get("plazo_entrega_dias", 0)

    motivos = []
    pasa = True

    # Filtro: rango de presupuesto (ejemplo: entre 1,000,000 y 500,000,000 CRC)
    if presupuesto < 1_000_000 or presupuesto > 500_000_000:
        motivos.append(
            f"Presupuesto fuera de rango: {presupuesto} (esperado entre 1,000,000 y 500,000,000 CRC)"
        )
        pasa = False

    # Filtro: industria o línea de negocio TI afines
    industrias_validas = ["TI", "Tecnología", "Sistemas", "Informática", "Software"]
    if industria not in industrias_validas and "TI" not in linea_negocio.upper():
        motivos.append(
            f"Industria o línea de negocio no TI: industria={industria}, línea={linea_negocio}"
        )
        pasa = False

    # Filtro: plazo de entrega razonable (mínimo 30 días)
    if plazo_entrega < 30:
        motivos.append(
            f"Plazo de entrega muy corto: {plazo_entrega} días (mínimo 30)"
        )
        pasa = False

    return {
        "regla": "R2 - Filtros duros iniciales",
        "numero_cartel": cartel.get("numero_cartel", "N/A"),
        "pasa_filtros": pasa,
        "motivos": motivos,
        "presupuesto_estimado": presupuesto,
        "industria": industria,
        "linea_negocio": linea_negocio,
        "plazo_entrega_dias": plazo_entrega,
    }
