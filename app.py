from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


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
