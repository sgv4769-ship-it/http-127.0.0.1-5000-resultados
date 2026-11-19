"""Paquete principal de la aplicación Flask."""
import os
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash


def requiere_login(vista):
    """Decorador que exige autenticación para acceder a una ruta.

    Si el usuario no tiene sesión activa, redirige a /login.
    También expira la sesión tras 5 minutos de inactividad.
    Esta es la regla de acceso del controlador (AGENTS.md).
    """
    def envoltura(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("login", next=request.path))

        # Expiración de sesión por inactividad: 5 minutos (300 segundos)
        ultima = session.get("ultima_actividad")
        if ultima is not None:
            inactivo = time.time() - ultima
            if inactivo > 300:
                session.clear()
                flash("Sesión expirada por inactividad (5 minutos).", "error")
                return redirect(url_for("login", next=request.path))

        # Actualizar marca de actividad en cada request protegido
        session["ultima_actividad"] = time.time()
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

    # Llave secreta obligatoria: sin valor por defecto inseguro.
    # Debe definirse en .env local o en variables de entorno de Render.
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY no está definida. "
            "Configúrala en .env (local) o en Environment Variables (Render)."
        )
    app.secret_key = secret_key

    # Cookies de sesión seguras: protegen contra robo e intercepción.
    # En Render (HTTPS) se activa Secure. En localhost se permite sin Secure para pruebas.
    es_produccion = os.environ.get("FLASK_ENV", "development") == "production"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = es_produccion

    # Usuario y contraseña válidos (lee de variables de entorno)
    USUARIO_VALIDO = os.environ.get("APP_USUARIO", "")
    CLAVE_VALIDA = os.environ.get("APP_CLAVE", "")

    # Control de intentos fallidos por IP (memoria en servidor, se reinicia al reiniciar app)
    intentos_fallidos = {}

    def _registro_intento_fallido(ip: str) -> int:
        ahora = time.time()
        registro = intentos_fallidos.get(ip, {"conteo": 0, "bloqueado_hasta": 0})
        if ahora < registro["bloqueado_hasta"]:
            return registro["conteo"]
        registro["conteo"] += 1
        registro["bloqueado_hasta"] = 0
        intentos_fallidos[ip] = registro
        return registro["conteo"]

    def _bloquear_ip(ip: str, minutos: int = 15):
        ahora = time.time()
        intentos_fallidos[ip] = {
            "conteo": 0,
            "bloqueado_hasta": ahora + (minutos * 60),
        }

    def _esta_bloqueado(ip: str) -> bool:
        registro = intentos_fallidos.get(ip)
        if not registro:
            return False
        ahora = time.time()
        if ahora < registro["bloqueado_hasta"]:
            return True
        # Ya pasó el tiempo de bloqueo, limpiar
        intentos_fallidos.pop(ip, None)
        return False

    # Ruta de login - muestra formulario y valida credenciales
    @app.route("/login", methods=["GET", "POST"])
    def login():
        ip = request.remote_addr or "desconocida"

        if _esta_bloqueado(ip):
            flash("Demasiados intentos fallidos. Intente nuevamente en 15 minutos.", "error")
            return render_template("login.html", bloqueado=True)

        if request.method == "POST":
            usuario = request.form.get("usuario", "")
            clave = request.form.get("clave", "")

            if usuario == USUARIO_VALIDO and clave == CLAVE_VALIDA:
                # Éxito: limpiar intentos fallidos y crear sesión
                intentos_fallidos.pop(ip, None)
                session["usuario"] = usuario
                session["ultima_actividad"] = time.time()
                pagina_destino = request.args.get("next", url_for("inicio"))
                return redirect(pagina_destino)
            else:
                # Fallo: registrar intento y bloquear si llega a 3
                conteo = _registro_intento_fallido(ip)
                if conteo >= 3:
                    _bloquear_ip(ip, minutos=15)
                    flash("Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos.", "error")
                else:
                    restantes = 3 - conteo
                    flash(
                        f"Usuario o contraseña incorrectos. "
                        f"Le quedan {restantes} intento(s) antes del bloqueo.",
                        "error",
                    )
        return render_template("login.html")

    # Ruta de salir - cierra la sesión
    @app.route("/salir")
    def salir():
        session.clear()
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
