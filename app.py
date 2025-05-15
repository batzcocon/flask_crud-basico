from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
import os



app = Flask(__name__)
app.secret_key = 'clave_secreta'


#iniciando base de datos:
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute(""" 
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre TEXT NOT NULL,
                       edad INTEGER NOT NULL,
                       correo TEXT NOT NULL
                       )""")
    conn.commit()
    conn.close()
    

#endpoint principal. 
@app.route("/")
def home():
    return render_template('formulario.html')


#endpoint para mostrar el saludo y guardar el dato.
@app.route('/saludo', methods=['POST'])
def saludo():
    nombre = request.form['nombre']
    edad = request.form['edad']
    correo = request.form['correo']
    #guardando en la base de datos:
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, edad, correo) VALUES (?,?,?)",(nombre,edad,correo))
    conn.commit()
    conn.close()
    flash(f"Usuario {nombre} registrado exitosamente.", "success")
    return redirect(url_for("home"))


#endpoint para mostrar los usuarios agregados.
@app.route('/usuarios')
def mostrar_usuarios():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, edad, correo FROM usuarios ')
    nombres = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html',lista = nombres)


#endpoint para eliminar usuarios
@app.route('/eliminar/<int:id>')
def eliminar_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Para saber el nombre antes de eliminar
    cursor.execute("SELECT nombre FROM usuarios WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    nombre = resultado[0] if resultado else "Usuario"
    
    cursor.execute('DELETE FROM usuarios WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    flash(f"{nombre} ha sido eliminado correctamente.", "warning")
    return redirect(url_for("mostrar_usuarios"))


#endpoint para editar los datos.
@app.route("/editar/<int:id>", methods=["GET"])
def editar_usuario(id):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, edad, correo FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()
    return render_template("editar.html", id=id, nombre=usuario[0], edad=usuario[1], correo=usuario[2])


#endpoint para actualizar datos
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar_usuario(id):
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    correo = request.form["correo"]

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, edad = ?, correo = ?
        WHERE id = ?
    """, (nombre, edad, correo, id))
    conn.commit()
    conn.close()
    flash(f"Los datos de {nombre} se actualizaron correctamente.", "info")
    return redirect(url_for("mostrar_usuarios"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provee el puerto como variable de entorno
    init_db()
    app.run(host="0.0.0.0", port=port)

    
