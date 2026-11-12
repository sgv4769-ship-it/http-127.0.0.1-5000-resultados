"""Paquete principal de la aplicación Flask."""
from flask import Flask, render_template


def create_app() -> Flask:
    """Crea y configura la aplicación Flask.

    Registra los blueprints de los controladores y carga la configuración.
    """
    app = Flask(__name__)

    # Cargar configuración desde variables de entorno (.env)
    app.config.from_prefixed_env()

    # Ruta principal - pantalla de inicio
    @app.route("/")
    def inicio():
        return render_template("inicio.html")

    # Ruta de resultados - tablero con contadores y tabla
    @app.route("/resultados")
    def resultados():
        return render_template("resultados.html")

    @app.route("/health")
    def health():
        return {"estado": "activa", "servicio": "analisis-carteles-sicop"}

    return app
