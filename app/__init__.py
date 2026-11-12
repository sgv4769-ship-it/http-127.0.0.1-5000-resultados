"""Paquete principal de la aplicación Flask."""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash


def requiere_login(vista):
    """Decorador que exige autenticación para acceder a una ruta.

    Si el usuario no tiene sesión activa, redirige a /login.
    Esta es la regla de acceso del controlador (AGENTS.md).
    """
    def envoltura(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("login", next=request.path))
        return vista(*args, **kwargs)
    envoltura.__name__ = vista.__name__
    return envoltura


def create_app() -> Flask:
    """Crea y configura la aplicación Flask.

    Registra los blueprints de los controladores y carga la configuración.
    """
    app = Flask(__name__)

    # Cargar configuración desde variables de entorno (.env)
    app.config.from_prefixed_env()

    # Llave secreta para sesiones de Flask (lee de SECRET_KEY en .env)
    app.secret_key = os.environ.get("SECRET_KEY", "cambiar_en_produccion")

    # Usuario y contraseña válidos (lee de variables de entorno)
    USUARIO_VALIDO = os.environ.get("APP_USUARIO", "")
    CLAVE_VALIDA = os.environ.get("APP_CLAVE", "")

    # Ruta de login - muestra formulario y valida credenciales
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("usuario", "")
            clave = request.form.get("clave", "")

            if usuario == USUARIO_VALIDO and clave == CLAVE_VALIDA:
                session["usuario"] = usuario
                pagina_destino = request.args.get("next", url_for("inicio"))
                return redirect(pagina_destino)
            else:
                flash("Usuario o contraseña incorrectos", "error")
        return render_template("login.html")

    # Ruta de salir - cierra la sesión
    @app.route("/salir")
    def salir():
        session.pop("usuario", None)
        return redirect(url_for("login"))

    # Ruta principal - pantalla de inicio (requiere login)
    @app.route("/")
    @requiere_login
    def inicio():
        return render_template("inicio.html")

    # Ruta de resultados - tablero con contadores y tabla (requiere login)
    @app.route("/resultados")
    @requiere_login
    def resultados():
        return render_template("resultados.html")

    # Ruta de salud pública (no requiere login para que Render pueda hacer health check)
    @app.route("/health")
    def health():
        return {"estado": "activa", "servicio": "analisis-carteles-sicop"}

    return app
