// Fungsi yang dijalankan saat halaman selesai dimuat
document.addEventListener('DOMContentLoaded', function() {
    loadItems();  // Muat daftar ATK
    setDefaultMonth();  // Set bulan default untuk laporan
    
    // Event listener untuk form tambah item
    document.getElementById('addItemForm').addEventListener('submit', addItem);
});

// Fungsi untuk menampilkan tab
function showTab(tabName) {
    // Sembunyikan semua tab
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Nonaktifkan semua tombol tab
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));
    
    // Tampilkan tab yang dipilih
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // Load report jika tab report dibuka
    if (tabName === 'report') {
        loadReport();
    }
}

// Fungsi untuk memuat daftar ATK dari server
async function loadItems() {
    try {
        // Fetch data dari API
        const response = await fetch('/api/items');
        const items = await response.json();
        
        // Tampilkan di HTML
        const itemsList = document.getElementById('itemsList');
        
        if (items.length === 0) {
            itemsList.innerHTML = '<p>Belum ada item ATK. Tambahkan item baru di atas.</p>';
            return;
        }
        
        itemsList.innerHTML = items.map(item => `
            <div class="item-card">
                <div class="item-header">
                    <div>
                        <div class="item-name">${item.name}</div>
                        <div style="color: #666; font-size: 0.9em;">Satuan: ${item.unit}</div>
                    </div>
                    <div class="item-stock">${item.stock} ${item.unit}</div>
                </div>
                <div class="item-actions">
                    <button class="btn-in" onclick="updateStock(${item.id}, 'in')">
                        ➕ Tambah Stok
                    </button>
                    <button class="btn-out" onclick="updateStock(${item.id}, 'out')">
                        ➖ Kurangi Stok
                    </button>
                    <button class="btn-delete" onclick="deleteItem(${item.id})">
                        🗑️ Hapus
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading items:', error);
        alert('Gagal memuat data ATK');
    }
}

// Fungsi untuk menambah item baru
async function addItem(e) {
    e.preventDefault();  // Mencegah form reload halaman
    
    // Ambil data dari form
    const name = document.getElementById('itemName').value;
    const stock = parseInt(document.getElementById('itemStock').value);
    const unit = document.getElementById('itemUnit').value;
    
    try {
        // Kirim data ke server
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, stock, unit })
        });
        
        if (response.ok) {
            alert('Item berhasil ditambahkan!');
            // Reset form
            document.getElementById('addItemForm').reset();
            // Reload daftar item
            loadItems();
        } else {
            alert('Gagal menambahkan item');
        }
        
    } catch (error) {
        console.error('Error adding item:', error);
        alert('Terjadi kesalahan');
    }
}

// Fungsi untuk update stok (tambah/kurang)
async function updateStock(itemId, type) {
    // Prompt untuk input jumlah
    const quantity = prompt(`Masukkan jumlah yang ingin ${type === 'in' ? 'ditambahkan' : 'dikurangi'}:`);
    
    if (!quantity || quantity <= 0) {
        return;
    }
    
    const note = prompt('Catatan (opsional):') || '';
    
    try {
        const response = await fetch(`/api/items/${itemId}/stock`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                type, 
                quantity: parseInt(quantity),
                note 
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(`Stok berhasil ${type === 'in' ? 'ditambahkan' : 'dikurangi'}! Stok baru: ${result.new_stock}`);
            loadItems();
        } else {
            alert(result.error || 'Gagal update stok');
        }
        
    } catch (error) {
        console.error('Error updating stock:', error);
        alert('Terjadi kesalahan');
    }
}

async function deleteItem(itemId) {
    if (!confirm('Yakin ingin menghapus item ini?')) {
        return;
    }

    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json'
            }
        });

        if (response.ok) {
            alert('Item berhasil dihapus!');
            loadItems();
        } else {
            alert('Gagal menghapus item')
        }
    } catch (error) {
        console.error('Error deleting item:', error);
        alert('terjadi kesalahan');
    }
}


// Set bulan default untuk input laporan
function setDefaultMonth() {
    const today = new Date();
    const month = today.toISOString().substring(0, 7);
    document.getElementById('reportMonth').value = month;
}

// Fungsi untuk memuat laporan bulanan
async function loadReport() {
    const month = document.getElementById('reportMonth').value;
    
    try {
        const response = await fetch(`/api/reports/monthly?month=${month}`);
        const report = await response.json();
        
        const reportContent = document.getElementById('reportContent');
        
        if (report.length === 0) {
            reportContent.innerHTML = '<p>Belum ada data untuk bulan ini.</p>';
            return;
        }
        
        reportContent.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Nama Item</th>
                        <th>Satuan</th>
                        <th>Total Ditambahkan</th>
                        <th>Total Digunakan</th>
                    </tr>
                </thead>
                <tbody>
                    ${report.map(item => `
                        <tr>
                            <td>${item.name}</td>
                            <td>${item.unit}</td>
                            <td style="color: #48bb78; font-weight: 600;">+${item.total_added}</td>
                            <td style="color: #f56565; font-weight: 600;">-${item.total_used}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error loading report:', error);
        alert('Gagal memuat laporan');
    }
}