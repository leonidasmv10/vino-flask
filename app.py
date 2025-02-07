from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.urandom(24)


def conectarBD(
    host: str, port: str, user: str, password: str, database: str
) -> mysql.connector.connection.MySQLConnection:
    try:
        mydb = mysql.connector.connect(
            host=host, port=port, user=user, password=password, database=database
        )
        if mydb.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
            return mydb
        else:
            print("No se pudo conectar a la base de datos MySQL")
            return None
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None


@app.route("/")
def tienda():
    tipo_filtro = request.args.get("tipo")
    print(f"Tipo de filtro: {tipo_filtro}")
    mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
    if mydb:
        try:
            mycursor = mydb.cursor()
            if tipo_filtro:
                print(f"Aplicando filtro por tipo: {tipo_filtro}")
                mycursor.execute(
                    "SELECT * FROM vinos WHERE categoria=%s", (tipo_filtro,)
                )

            else:
                mycursor.execute("SELECT * FROM vinos")

            vinos = mycursor.fetchall()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            vinos = []
        finally:
            mydb.close()
    else:
        vinos = []
    return render_template("home.html", vinos=vinos, es_admin=es_admin)


@app.route("/agregar_vino", methods=["GET", "POST"])
def agregar_vino():
    if "user_id" not in session or not es_admin(session["user_id"]):
        return redirect(url_for("tienda"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        categoria = request.form["categoria"]
        imagen = request.form["imagen"]
        stock = request.form["stock"]

        mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
        if mydb:
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO vinos (nombre, descripcion, precio, categoria, imagen, stock) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (nombre, descripcion, precio, categoria, imagen, stock)
                mycursor.execute(sql, val)
                mydb.commit()
                print("Vino agregado correctamente")
                return redirect(url_for("home"))  # Redirigir a la página principal
            except Error as e:
                print(f"Error al agregar el vino: {e}")
            finally:
                mydb.close()

    return render_template("agregar_vino.html", es_admin=es_admin)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        is_admin = "is_admin" in request.form  # Verifica si el checkbox está marcado

        # Hash de la contraseña
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
        if mydb:
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO usuarios (username, password, is_admin) VALUES (%s, %s, %s)"
                val = (
                    username,
                    hashed_password,
                    is_admin,
                )  # Incluir is_admin en la inserción
                mycursor.execute(sql, val)
                mydb.commit()
                print("Usuario registrado correctamente")
                return redirect(url_for("login"))
            except Error as e:
                print(f"Error al registrar el usuario: {e}")
            finally:
                mydb.close()

    return render_template("register.html", es_admin=es_admin)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
        if mydb:
            try:
                mycursor = mydb.cursor()
                mycursor.execute(
                    "SELECT * FROM usuarios WHERE username = %s", (username,)
                )
                user = mycursor.fetchone()
                if user and check_password_hash(
                    user[2], password
                ):  # Verifica la contraseña hasheada
                    session["user_id"] = user[
                        0
                    ]  # Guarda el ID del usuario en la sesión
                    session["username"] = user[1]
                    print("Usuario logueado correctamente")
                    return redirect(url_for("home"))  # Redirige a la página principal
                else:
                    print("Credenciales incorrectas")
            except Error as e:
                print(f"Error al iniciar sesión: {e}")
            finally:
                mydb.close()

    return render_template("login.html", es_admin=es_admin)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/eliminar_vino/<int:vino_id>")
def eliminar_vino(vino_id):
    if "user_id" not in session or not es_admin(session["user_id"]):
        return redirect(url_for("tienda"))  # Redirige si no es admin
    mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
    if mydb:
        try:
            mycursor = mydb.cursor()
            sql = "DELETE FROM vinos WHERE id = %s"
            val = (vino_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Vino eliminado correctamente")
            return redirect(url_for("tienda"))
        except Error as e:
            print(f"Error al eliminar el vino: {e}")
        finally:
            mydb.close()
    return redirect(url_for("tienda"))


# ... (código anterior sin cambios)


@app.route("/modificar_vino/<int:vino_id>", methods=["GET", "POST"])
def modificar_vino(vino_id):
    if "user_id" not in session or not es_admin(session["user_id"]):
        return redirect(url_for("tienda"))  # Redirige si no es admin

    mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
    if mydb:
        try:
            mycursor = mydb.cursor()

            if request.method == "POST":  # Manejar el POST antes que el GET
                nombre = request.form["nombre"]
                descripcion = request.form["descripcion"]
                precio = request.form["precio"]
                categoria = request.form["categoria"]
                imagen = request.form["imagen"]
                stock = request.form["stock"]

                # Actualizar datos del vino en la base de datos
                sql = "UPDATE vinos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, imagen = %s, stock = %s WHERE id = %s"
                val = (nombre, descripcion, precio, categoria, imagen, stock, vino_id)
                mycursor.execute(sql, val)
                mydb.commit()

                print("Vino modificado correctamente")
                return redirect(url_for("tienda"))  # Redirigir a la página de la tienda
            else:  # GET request: Mostrar el formulario con los datos del vino
                mycursor.execute("SELECT * FROM vinos WHERE id = %s", (vino_id,))
                vino = mycursor.fetchone()
                print(type(vino))
                if vino:  # Si existe el vino
                    return render_template("modificar_vino.html", vino=vino)
                else:  # Si no existe el vino
                    return "Vino no encontrado"  # O podrías redirigir a una página de error

        except Error as e:
            print(f"Error al modificar el vino: {e}")
        finally:
            mydb.close()

    return redirect(url_for("home"))


def es_admin(usuario_id):
    mydb = conectarBD("localhost", "3306", "root", "1234", "tiendavinosdb")
    if mydb:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT is_admin FROM usuarios WHERE id = %s", (usuario_id,)
            )
            resultado = mycursor.fetchone()
            return resultado[0] if resultado else False  # True si es admin, False si no
        except Error as e:
            print(f"Error al verificar admin: {e}")
            return False
        finally:
            mydb.close()
    return False


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]
        return redirect(url_for("success", nombre=nombre, email=email, mensaje=mensaje))
    return render_template("contact.html")


@app.route("/success")
def success():
    nombre = request.args.get("nombre")
    email = request.args.get("email")
    mensaje = request.args.get("mensaje")
    return render_template("success.html", nombre=nombre, email=email, mensaje=mensaje)


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV")
    if env == "development":
        app.run(debug=True)
    else:
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)
