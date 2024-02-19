from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"
ruta_archivo = os.path.join("data", "estado.json")

def cargar_datos(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = {
            "lista": [
                {"nombre": "Agus", "contribuciones": 0},
                {"nombre": "Jose", "contribuciones": 0},
                {"nombre": "Kari", "contribuciones": 0},
                {"nombre": "María", "contribuciones": 0},
                {"nombre": "Moi", "contribuciones": 0},
                {"nombre": "Mónica", "contribuciones": 0}
            ],
            "indice_actual": 0
        }
    return datos


@app.route('/', methods=["GET", "POST"])
def home():
    datos = cargar_datos(ruta_archivo)
    es_solicitud_post = False
    if request.method == "POST":
        if request.form["action"] == "marcar":
            datos["lista"][datos["indice_actual"]]["contribuciones"] += 1
            datos["indice_actual"] = (datos["indice_actual"] + 1) % len(datos["lista"])
            print("índice incrementado")
        elif request.form["action"] == "saltar":
            if datos["indice_actual"] < len(datos["lista"]) - 1:
                datos["lista"].append(datos["lista"].pop(datos["indice_actual"]))
            else:
                datos["indice_actual"] = 0
        print("antes de guardar los datos")
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False)
        print("después del guardado")
        session['es_solicitud_post'] = True
        return redirect(url_for("home"))
    es_solicitud_post = session.pop("es_solicitud_post", False)
    print(datos["lista"])  # Debería mostrar una lista de diccionarios
    print(datos["indice_actual"])  # Debería mostrar un entero

    return render_template("index.html", proximo=datos["lista"][datos["indice_actual"]]["nombre"], datos=datos, es_solicitud_post=es_solicitud_post)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
