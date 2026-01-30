# Import library yang dibutuhkan
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Fungsi untuk koneksi ke database
def get_db():
    """
    Membuat koneksi ke database SQLite
    SQLite adalah database file sederhana, tidak perlu install server
    """
    conn = sqlite3.connect('atk.db')
    conn.row_factory = sqlite3.Row  # Agar hasil query bisa diakses seperti dictionary
    return conn

# Fungsi untuk membuat tabel database pertama kali
def init_db():
    """
    Membuat tabel-tabel yang dibutuhkan jika belum ada
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabel untuk menyimpan data ATK
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            unit TEXT NOT NULL
        )
    ''')
    
    # Tabel untuk menyimpan riwayat transaksi (penambahan/pengurangan)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Route untuk halaman utama
@app.route('/')
def index():
    """
    Menampilkan halaman utama dashboard
    """
    return render_template('index.html')

# API untuk mendapatkan semua data ATK
@app.route('/api/items', methods=['GET'])
def get_items():
    """
    Endpoint API untuk mengambil semua data ATK
    Method: GET
    Return: JSON array berisi semua item ATK
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items ORDER BY name')
    items = cursor.fetchall()
    conn.close()
    
    # Konversi hasil query ke list of dict
    items_list = []
    for item in items:
        items_list.append({
            'id': item['id'],
            'name': item['name'],
            'stock': item['stock'],
            'unit': item['unit']
        })
    
    return jsonify(items_list)

# API untuk menambah item ATK baru
@app.route('/api/items', methods=['POST'])
def add_item():
    """
    Endpoint API untuk menambah item ATK baru
    Method: POST
    Body: JSON {name, stock, unit}
    """
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO items (name, stock, unit) VALUES (?, ?, ?)',
        (data['name'], data['stock'], data['unit'])
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': item_id, 'message': 'Item berhasil ditambahkan'}), 201

# API untuk update stok (tambah/kurang)
@app.route('/api/items/<int:item_id>/stock', methods=['PUT'])
def update_stock(item_id):
    """
    Endpoint API untuk menambah atau mengurangi stok
    Method: PUT
    Parameter: item_id (ID item yang akan diupdate)
    Body: JSON {type: 'in'/'out', quantity, note}
    """
    data = request.get_json()
    transaction_type = data['type']  # 'in' untuk tambah, 'out' untuk kurang
    quantity = int(data['quantity'])
    note = data.get('note', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Ambil stok saat ini
    cursor.execute('SELECT stock FROM items WHERE id = ?', (item_id,))
    current_stock = cursor.fetchone()['stock']
    
    # Hitung stok baru
    if transaction_type == 'in':
        new_stock = current_stock + quantity
    else:  # 'out'
        new_stock = current_stock - quantity
        if new_stock < 0:
            conn.close()
            return jsonify({'error': 'Stok tidak cukup'}), 400
    
    # Update stok
    cursor.execute('UPDATE items SET stock = ? WHERE id = ?', (new_stock, item_id))
    
    # Catat transaksi
    cursor.execute(
        'INSERT INTO transactions (item_id, type, quantity, date, note) VALUES (?, ?, ?, ?, ?)',
        (item_id, transaction_type, quantity, datetime.now().isoformat(), note)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Stok berhasil diupdate', 'new_stock': new_stock})

# API untuk mendapatkan laporan penggunaan per bulan
@app.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    """
    Endpoint API untuk mendapatkan laporan penggunaan bulanan
    Method: GET
    Query Parameter: month (format: YYYY-MM)
    """
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Query untuk mendapatkan total penggunaan per item di bulan tertentu
    cursor.execute('''
        SELECT 
            i.name,
            i.unit,
            SUM(CASE WHEN t.type = 'out' THEN t.quantity ELSE 0 END) as total_used,
            SUM(CASE WHEN t.type = 'in' THEN t.quantity ELSE 0 END) as total_added
        FROM items i
        LEFT JOIN transactions t ON i.id = t.item_id
        WHERE t.date LIKE ? || '%' OR t.date IS NULL
        GROUP BY i.id, i.name, i.unit
        ORDER BY i.name
    ''', (month,))
    
    results = cursor.fetchall()
    conn.close()
    
    report = []
    for row in results:
        report.append({
            'name': row['name'],
            'unit': row['unit'],
            'total_used': row['total_used'] or 0,
            'total_added': row['total_added'] or 0
        })
    
    return jsonify(report)

# Jalankan aplikasi
if __name__ == '__main__':
    init_db()  # Inisialisasi database
    app.run(host='0.0.0.0', port=5000, debug=True)