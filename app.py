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
            mid TEXT NOT NULL UNIQUE,
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
            'mid': item['mid'],
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
        'INSERT INTO items (mid, name, stock, unit) VALUES (?, ?, ?, ?)',
        (data['mid'], data['name'], data['stock'], data['unit'])
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
    Body: JSON {type: 'in'/'out', quantity, date}
    """
    data = request.get_json()
    transaction_type = data['type']  # 'in' untuk tambah, 'out' untuk kurang
    quantity = int(data['quantity'])
    transaction_date = data.get('date', datetime.now().isoformat())
    
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
        'INSERT INTO transactions (item_id, type, quantity, date) VALUES (?, ?, ?, ?)',
        (item_id, transaction_type, quantity, transaction_date)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Stok berhasil diupdate', 'new_stock': new_stock})

# API untuk menghapus item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Endpoint API untuk menghapus item ATK
    Method: DELETE
    Parameter: item_id (ID item yang akan dihapus)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Hapus transaksi terkait item terlebih dahulu
    cursor.execute('DELETE FROM transactions WHERE item_id = ?', (item_id,))
    
    # Hapus item
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item berhasil dihapus'})

# API untuk mendapatkan laporan penggunaan per bulan
# API untuk mendapatkan laporan penggunaan per bulan
@app.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    """
    Endpoint API untuk mendapatkan laporan penggunaan bulanan
    Method: GET
    Query Parameter: month (format: YYYY-MM)
    """
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    # Validasi format month
    try:
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        return jsonify({'error': 'Format bulan tidak valid'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Query untuk mendapatkan semua item dan transaksi mereka di bulan tertentu
    cursor.execute('''
        SELECT 
            i.id,
            i.mid,
            i.name,
            i.unit,
            t.id as transaction_id,
            t.type,
            t.quantity,
            t.date
        FROM items i
        LEFT JOIN transactions t ON i.id = t.item_id 
            AND t.date LIKE ? || '%'
        ORDER BY i.name, t.date DESC
    ''', (month,))
    
    results = cursor.fetchall()
    conn.close()

    # Kelompokkan data per item
    report_dict = {}
    for row in results:
        item_key = row['id']

        if item_key not in report_dict:
            report_dict[item_key] = {
                'mid': row['mid'],
                'name': row['name'],
                'unit': row['unit'],
                'total_used': 0,
                'total_added': 0,
                'transactions': []
            }

        # Jika ada transaksi
        if row['transaction_id']:
            transaction = {
                'type': row['type'],
                'quantity': row['quantity'],
                'date': row['date']
            }
            report_dict[item_key]['transactions'].append(transaction)

            # Hitung total
            if row['type'] == 'out':
                report_dict[item_key]['total_used'] += row['quantity']
            elif row['type'] == 'in':
                report_dict[item_key]['total_added'] += row['quantity']
    
    # Konversi ke list
    report = list(report_dict.values())
    
    return jsonify(report)

# Jalankan aplikasi
if __name__ == '__main__':
    init_db()  # Inisialisasi database
    app.run(host='0.0.0.0', port=5000, debug=True)