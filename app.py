from flask import Flask, render_template
import os
app  = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 10000))  # Render asigna un puerto automáticamente
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)