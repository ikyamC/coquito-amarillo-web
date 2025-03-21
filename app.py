from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import json

app = Flask(__name__)

# Conexión a MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="coquito"
)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/evaluacion', methods=['GET', 'POST'])
def evaluacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        puntaje = request.form['puntaje']

        # Guardar en JSON
        with open('datos.json', 'a') as archivo:
            json.dump({'nombre': nombre, 'correo': correo, 'puntaje': puntaje}, archivo)
            archivo.write("\n")

        # Guardar en MySQL
        cursor = db.cursor()
        cursor.execute("INSERT INTO Encuesta (nombre, correo, puntaje) VALUES (%s, %s, %s)", (nombre, correo, puntaje))
        db.commit()
        cursor.close()

        return redirect(url_for('inicio'))
    
    return render_template('evaluacion.html')

if __name__ == '__main__':
    app.run(debug=True)
