import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="your_database",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price, image_url, is_featured FROM products;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        is_featured = 'is_featured' in request.form
        
        image = request.files['image']
        image_url = ""
        
        if image and image.filename != '':
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f'uploads/{filename}'
            
        cur.execute(
            'INSERT INTO products (name, description, price, image_url, is_featured) VALUES (%s, %s, %s, %s, %s);',
            (name, description, price, image_url, is_featured)
        )
        conn.commit()
        
    cur.execute('SELECT id, name, description, price, image_url, is_featured FROM products;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('admin.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
