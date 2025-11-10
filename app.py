from flask import Flask, jsonify
import os
import platform
import psutil

# Expor a app como APP para gunicorn: gunicorn app:APP
APP = Flask(__name__)

# Coloque aqui os nomes dos integrantes
INTEGRANTES = [
    "Seu Nome Completo",
    "Nome do Segundo Integrante"  # remova/adicione conforme necessário
]

def coletar_metricas():
    p = psutil.Process(os.getpid())
    pid = p.pid
    memoria_mb = p.memory_info().rss / (1024 * 1024)  # em MB
    # cpu_percent: chama-se com pequeno intervalo para medir
    cpu_pct = p.cpu_percent(interval=0.1)
    so = platform.system() + (" (" + platform.platform() + ")" )
    return {
        "PID": pid,
        "Memoria_MB": round(memoria_mb, 2),
        "CPU_percent": round(cpu_pct, 2),
        "Sistema_Operacional": so
    }

@APP.route("/info")
def rota_info():
    # Retorna apenas os nomes (formato JSON)
    return jsonify({"integrantes": INTEGRANTES})

@APP.route("/metricas")
def rota_metricas():
    m = coletar_metricas()
    return jsonify(m)

if __name__ == "__main__":
    # Execução local para testes
    APP.run(host="0.0.0.0", port=8080, debug=True)
