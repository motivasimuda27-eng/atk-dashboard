# Import library yang dibutuhkan
from flask import Flask, render_template, request, jsonify, make_response
import sqlite3
from datetime import datetime
import os
from contextlib import contextmanager
import csv
from io import StringIO

# Inisialisasi aplikasi Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

#context manager untuk koneksi database
@contextmanager
def get_db_connection():
    """
    Context manager untuk koneksi database SQLite.
    koneksi akan otomatis ditutup meski terjadi error.
    """
    conn = sqlite3.connect('atk.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

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
            unit TEXT NOT NULL,
            storage_location TEXT DEFAULT ''
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
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items ORDER BY name')
            items = cursor.fetchall()
            
            items_list = [{
                'id': item['id'],
                'mid': item['mid'],
                'name': item['name'],
                'stock': item['stock'],
                'unit': item['unit'],
                'storage_location': item['storage_location']
            } for item in items]
            
            return jsonify(items_list)
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

# API untuk menambah item ATK baru
@app.route('/api/items', methods=['POST'])
def add_item():
    """
    Endpoint API untuk menambah item ATK baru
    """
    try:
        data = request.get_json()
        
        # Validasi request body
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        # Validasi required fields
        required_fields = ['mid', 'name', 'stock', 'unit']
        missing = [f for f in required_fields if f not in data or data[f] == '']
        if missing:
            return jsonify({'error': f'Field wajib diisi: {", ".join(missing)}'}), 400
        
        # Validasi tipe data stock
        try:
            stock = int(data['stock'])
            if stock < 0:
                return jsonify({'error': 'Stock tidak boleh negatif'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Stock harus berupa angka'}), 400
        
        # Validasi panjang input
        if len(data['mid']) > 50:
            return jsonify({'error': 'MID maksimal 50 karakter'}), 400
        if len(data['name']) > 100:
            return jsonify({'error': 'Nama maksimal 100 karakter'}), 400
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Cek duplikat MID
            cursor.execute('SELECT id FROM items WHERE mid = ?', (data['mid'],))
            if cursor.fetchone():
                return jsonify({'error': 'MID sudah digunakan'}), 400
            
            cursor.execute(
                'INSERT INTO items (mid, name, stock, unit, storage_location) VALUES (?, ?, ?, ?, ?)',
                (data['mid'].strip(), data['name'].strip(), stock, data['unit'].strip(), data.get('storage_location', '').strip())
            )
            conn.commit()
            item_id = cursor.lastrowid
            
        return jsonify({'id': item_id, 'message': 'Item berhasil ditambahkan'}), 201
        
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'MID sudah digunakan oleh item lain'}), 400
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500
# API untuk edit item
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def edit_item(item_id):
    """
    Endpoint API untuk mengubah data item ATK
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        # Validasi required fields
        required_fields = ['mid', 'name', 'stock', 'unit']
        missing = [f for f in required_fields if f not in data or data[f] == '']
        if missing:
            return jsonify({'error': f'Field wajib diisi: {", ".join(missing)}'}), 400
        
        # Validasi stock
        try:
            stock = int(data['stock'])
            if stock < 0:
                return jsonify({'error': 'Stock tidak boleh negatif'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Stock harus berupa angka'}), 400
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Cek apakah item ada
            cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            item = cursor.fetchone()
            
            if not item:
                return jsonify({'error': 'Item tidak ditemukan'}), 404
            
            # Cek duplikat MID
            cursor.execute('SELECT id FROM items WHERE mid = ? AND id != ?', (data['mid'], item_id))
            if cursor.fetchone():
                return jsonify({'error': 'MID sudah digunakan oleh item lain'}), 400
            
            cursor.execute('''
                UPDATE items 
                SET mid = ?, name = ?, stock = ?, unit = ?, storage_location = ?
                WHERE id = ?
            ''', (data['mid'].strip(), data['name'].strip(), stock, data['unit'].strip(), 
                  data.get('storage_location', '').strip(), item_id))
            
            conn.commit()
            
        return jsonify({'message': 'Item berhasil diperbarui'})
        
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

# API untuk update stok (tambah/kurang)
@app.route('/api/items/<int:item_id>/stock', methods=['PUT'])
def update_stock(item_id):
    """
    Endpoint API untuk menambah atau mengurangi stok
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        # Validasi type
        transaction_type = data.get('type')
        if transaction_type not in ['in', 'out']:
            return jsonify({'error': 'Type harus "in" atau "out"'}), 400
        
        # Validasi quantity
        try:
            quantity = int(data.get('quantity', 0))
            if quantity <= 0:
                return jsonify({'error': 'Quantity harus lebih dari 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Quantity harus berupa angka'}), 400
        
        transaction_date = data.get('date', datetime.now().isoformat())
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Ambil stok saat ini
            cursor.execute('SELECT stock, name FROM items WHERE id = ?', (item_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'error': 'Item tidak ditemukan'}), 404
            
            current_stock = row['stock']
            
            # Hitung stok baru
            if transaction_type == 'in':
                new_stock = current_stock + quantity
            else:
                new_stock = current_stock - quantity
                if new_stock < 0:
                    return jsonify({'error': f'Stok tidak cukup. Stok saat ini: {current_stock}'}), 400
            
            # Update stok
            cursor.execute('UPDATE items SET stock = ? WHERE id = ?', (new_stock, item_id))
            
            # Catat transaksi
            cursor.execute(
                'INSERT INTO transactions (item_id, type, quantity, date) VALUES (?, ?, ?, ?)',
                (item_id, transaction_type, quantity, transaction_date)
            )
            
            conn.commit()
            
        return jsonify({'message': 'Stok berhasil diupdate', 'new_stock': new_stock})
        
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

# API untuk menghapus item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Endpoint API untuk menghapus item ATK
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Cek apakah item ada
            cursor.execute('SELECT id FROM items WHERE id = ?', (item_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Item tidak ditemukan'}), 404
            
            # Hapus transaksi terkait
            cursor.execute('DELETE FROM transactions WHERE item_id = ?', (item_id,))
            
            # Hapus item
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            
            conn.commit()
            
        return jsonify({'message': 'Item berhasil dihapus'})
        
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

#API untuk bulk stock reservation
@app.route('/api/items/bulk_reservation', methods=['POST'])
def bulk_reservation():
    """
    Endpoint API untuk menambahkan stock beberapa item sekaligus
    Method: POST
    Body: JSON {items: [{item_id, quantity}], date}
    """
    data = request.get_json()
    items = data.get('items', [])
    transaction_date = data.get('date', datetime.now().isoformat())

    if not items:
        return jsonify({'error': 'Tidak ada item yang dipilih'}), 400
    
    conn = get_db()
    cursor = conn.cursor()

    results = []
    errors = []

    for item_data in items:
        item_id = item_data['item_id']
        quantity = int(item_data['quantity'])

        if quantity <= 0:
            continue

        try:
            #Ambil stock saat ini
            cursor.execute('SELECT stock, name FROM items WHERE id = ?', (item_id,))
            row = cursor.fetchone()

            if not row:
                errors.append(f"Item ID {item_id} tidak ditemukan")
                continue

            current_stock = row['stock']
            item_name = row['name']
            new_stock = current_stock + quantity

            #update stock
            cursor.execute('UPDATE items SET stock = ? WHERE id = ?', (new_stock, item_id))

            #catat transaksi
            cursor.execute(
                'INSERT INTO transactions (item_id, type, quantity, date) VALUES (?, ?, ?, ?)',
                (item_id, 'in', quantity, transaction_date)
            )

            results.append({
                'item_id': item_id,
                'name': item_name,
                'quantity': quantity,
                'new_stock': new_stock
            })
        
        except Exception as e:
            errors.append(f"Error pada item ID {item_id}: {str(e)}")
    
    conn.commit()
    conn.close()

    return jsonify({
        'message': f'Berhasil menambahkan stock {len(results)} item',
        'results': results,
        'errors': errors
    })



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
            i.storage_location,
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
                'storage_location': row['storage_location'],
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

@app.route('/api/reports/monthly/export', methods=['GET'])
def export_monthly_csv():
    """
    ENDPOINT API untuk export laporan bulanan ke CSV
    Method: GET
    Query Parameter: month (format: YYYY-MM)
    """
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    #validasi format month
    try:
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        return jsonify({'error': 'Format bulan tidak valid. gunakan YYYY-MM'}), 400
    
    conn = get_db()
    cursor = conn.cursor()

    # Query untuk mendapatkan semua item dan transaksi mereka di bulan tertentu
    cursor.execute('''
        SELECT 
            i.id,
            i.mid,
            i.name,
            i.unit,
            i.storage_location,
            t.id as transaction_id,
            t.type,
            t.quantity,
            t.date
        FROM items i
        LEFT JOIN transactions t ON i.id = t.item_id 
            AND t.date LIKE ? || '%'
        ORDER BY i.name, t.date
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
                'storage_location': row['storage_location'] or 'Belum ditentukan',
                'total_added': 0,
                'total_used': 0,
                'transactions': []
            }

        # Jika ada transaksi
        if row['transaction_id']:
            trans_data = {
                'date': row['date'],
                'type': row['type'],
                'quantity': row['quantity']
            }
            report_dict[item_key]['transactions'].append(trans_data)
            
            if row['type'] == 'in':
                report_dict[item_key]['total_added'] += row['quantity']
            else:
                report_dict[item_key]['total_used'] += row['quantity']
    
    # Konversi ke list
    report = list(report_dict.values())
    
    # Buat CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header CSV
    writer.writerow(['Tanggal Transaksi', 'MID', 'Nama Item', 'Satuan', 'Lokasi', 'Tipe', 'Jumlah', 'Total Reservasi', 'Total Digunakan'])
    
    # Data rows
    for item in report:
        if item['transactions']:
            for trans in item['transactions']:
                # Format tanggal
                try:
                    date_obj = datetime.fromisoformat(trans['date'].replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%d/%m/%y')
                except:
                    formatted_date = trans['date']
                
                type_label = 'Reservasi' if trans['type'] == 'in' else 'Digunakan'
                quantity_with_sign = f"+{trans['quantity']}" if trans['type'] == 'in' else f"-{trans['quantity']}"
                
                writer.writerow([
                    formatted_date,
                    item['mid'],
                    item['name'],
                    item['unit'],
                    item['storage_location'],
                    type_label,
                    quantity_with_sign,
                    item['total_added'],
                    item['total_used'],
                ])
        else:
            # Item tanpa transaksi
            writer.writerow([
                '-',
                item['mid'],
                item['name'],
                item['unit'],
                item['storage_location'],
                '-',
                '-',
                item['total_added'],
                item['total_used'],
            ])
    
    # Buat response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=laporan_atk_{month}.csv'
    
    return response

# Jalankan aplikasi
if __name__ == '__main__':
    init_db()  # Inisialisasi database
    app.run(host='0.0.0.0', port=5000, debug=True)