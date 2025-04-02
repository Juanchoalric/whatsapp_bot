import uvicorn
import webbrowser
import os
import time
from threading import Thread

def open_browser():
    """Abre el navegador después de un pequeño retraso"""
    time.sleep(2)
    url = "http://127.0.0.1:8081"
    print(f"Abriendo navegador en {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    # Iniciar thread para abrir el navegador
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Iniciar el servidor
    uvicorn.run("app.main:app", host="127.0.0.1", port=8081, reload=True) 