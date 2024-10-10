from flask import Flask, render_template, request, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import io
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('barcodes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



@app.route('/report', methods=['GET'])
def report():
    return render_template('report.html')

@app.route('/product', methods=['GET'])
def product():
    return render_template('product.html')

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        barcodes = decode(image)
        
        if barcodes:
            barcode_data = barcodes[0].data.decode('utf-8')
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM scans WHERE barcode = ?", (barcode_data,))
            result = c.fetchone()
            conn.close()

            if result:
                return jsonify({
                    'barcode': result['barcode'],
                    'name': result['name'],
                    'details': result['details'],
                    'timestamp': result['timestamp']
                })
            else:
                return jsonify({'barcode': barcode_data, 'message': 'Barcode not registered'})
        else:
            return jsonify({'error': 'No barcode found'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    barcode = data.get('barcode')
    name = data.get('name')
    details = data.get('details')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO scans VALUES (?, ?, ?, ?)", (barcode, name, details, timestamp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Barcode registered successfully'})

@app.route('/all', methods=['GET'])
def get_all():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM scans")
    results = c.fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    app.run(debug=True)
