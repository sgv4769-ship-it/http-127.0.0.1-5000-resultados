@echo off
:: Iniciar app de Analisis de Carteles SICOP
:: Abre el navegador y enciende la aplicación Flask

set FLASK_APP=wsgi.py
set FLASK_ENV=development

:: Iniciar la aplicación en segundo plano
start "" python -m flask run --host=127.0.0.1 --port=5000

:: Esperar un momento para que el servidor inicie
timeout /t 3 >nul

:: Abrir el navegador en la URL de la app
start "" http://127.0.0.1:5000/

echo Servidor Flask iniciado en http://127.0.0.1:5000/
echo Presione Ctrl+C para detener el servidor.
pause
