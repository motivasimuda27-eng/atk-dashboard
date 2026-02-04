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
                        <div style="color: #999; font-size: 0.85em;">MID: ${item.mid}</div>
                        <div class="item-name">${item.name}</div>
                        <div style="color: #666; font-size: 0.9em;">Satuan: ${item.unit}</div>
                        <div style="color: #666; font-size: 0.9em;">Lokasi: ${item.storage_location || 'Belum ditentukan'}</div>
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
                    <button class="btn-edit" onclick="editItem(${item.id}, '${item.mid}', '${item.name.replace(/'/g, "\\'")}', ${item.stock}, '${item.unit}', '${(item.storage_location || '').replace(/'/g, "\\'")}')">
                        ✏️ Edit
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
    const mid = document.getElementById('itemMID').value;
    const name = document.getElementById('itemName').value;
    const stock = parseInt(document.getElementById('itemStock').value);
    const unit = document.getElementById('itemUnit').value;
    const storage_location = document.getElementById('itemStorage').value;
    
    try {
        // Kirim data ke server
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({mid, name, stock, unit, storage_location})
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

// Variabel global untuk menyimpan data modal
let currentStockAction = { itemId: null, type: null };
let currentDeleteId = null;

// Fungsi untuk update stok (menampilkan modal)
function updateStock(itemId, type) {
    currentStockAction = { itemId, type };
    const title = type === 'in' ? 'Tambah Stok' : 'Kurangi Stok';
    document.getElementById('stockModalTitle').textContent = title;
    const today = new Date();
    const isoString = today.toISOString().slice(0, 10);
    document.getElementById('stockDate').value = isoString;
    document.getElementById('stockQuantity').value = '';
    document.getElementById('stockModal').classList.add('show');
    document.getElementById('stockQuantity').focus();
}

// Fungsi untuk menutup modal stock
function closeStockModal() {
    document.getElementById('stockModal').classList.remove('show');
    currentStockAction = { itemId: null, type: null };
}

// Fungsi untuk confirm stock
async function confirmStock() {
    const quantity = document.getElementById('stockQuantity').value;
    const stockDate = document.getElementById('stockDate').value;
    
    if (!quantity || quantity <= 0) {
        alert('Jumlah harus lebih dari 0');
        return;
    }

    if (!stockDate) {
        alert('Tanggal harus diisi');
        return;
    }
    
    const { itemId, type } = currentStockAction;
    const dateObj = new Date(stockDate);
    const isoDate = dateObj.toISOString();
    
    try {
        const response = await fetch(`/api/items/${itemId}/stock`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                type, 
                quantity: parseInt(quantity),
                date: isoDate
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(`Stok berhasil ${type === 'in' ? 'ditambahkan' : 'dikurangi'}! Stok baru: ${result.new_stock}`);
            closeStockModal();
            loadItems();
        } else {
            alert(result.error || 'Gagal update stok');
        }
        
    } catch (error) {
        console.error('Error updating stock:', error);
        alert('Terjadi kesalahan');
    }
}

// Fungsi untuk menghapus item (menampilkan modal)
function deleteItem(itemId) {
    currentDeleteId = itemId;
    document.getElementById('deleteModal').classList.add('show');
}

// Fungsi untuk menutup modal delete
function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('show');
    currentDeleteId = null;
}

// Fungsi untuk confirm delete
async function confirmDelete() {
    const itemId = currentDeleteId;
    
    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            alert('Item berhasil dihapus!');
            closeDeleteModal();
            loadItems();
        } else {
            alert('Gagal menghapus item');
        }
        
    } catch (error) {
        console.error('Error deleting item:', error);
        alert('Terjadi kesalahan');
    }
}

//fungsi untuk mengedit item (menampilkan modal)
function editItem(itemId, mid, name, stock, unit, storage) {
    document.getElementById('editItemId').value = itemId;
    document.getElementById('editMID').value = mid;
    document.getElementById('editName').value = name;
    document.getElementById('editStock').value = stock;
    document.getElementById('editUnit').value = unit;
    document.getElementById('editStorage').value = storage;
    document.getElementById('editModal').classList.add('show');
    document.getElementById('editMID').focus();
}

//fungsi untuk menutup modal edit
function closeEditModal() {
    document.getElementById('editModal').classList.remove('show');
}

//fungsi untuk mengonfirmasi edit item
async function confirmEdit() {
    const itemId = document.getElementById('editItemId').value;
    const mid = document.getElementById('editMID').value.trim();
    const name = document.getElementById('editName').value.trim();
    const stock = parseInt(document.getElementById('editStock').value);
    const unit = document.getElementById('editUnit').value.trim();
    const storage_location = document.getElementById('editStorage').value.trim();

    //validasi
    if (!mid || !name || !unit) {
        alert('MID, Nama, dan Satuan wajib diisi!');
        return;
    }
    
    if (stock < 0) {
        alert('Stock tidak boleh negatif!');
        return;
    }
    
    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mid, name, stock, unit, storage_location })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert('Item berhasil diperbarui!');
            closeEditModal();
            loadItems();
            loadAvailableItems(); // Refresh dropdown bulk reservation
        } else {
            alert(result.error || 'Gagal memperbarui item');
        }
        
    } catch (error) {
        console.error('Error editing item:', error);
        alert('Terjadi kesalahan');
    }
}

// Tutup modal saat klik di luar modal
window.onclick = function(event) {
    const stockModal = document.getElementById('stockModal');
    const deleteModal = document.getElementById('deleteModal');
    const bulkConfirmModal = document.getElementById('bulkConfirmModal');
    const editModal = document.getElementById('editModal');

    if (event.target === editModal) {
        closeEditModal();
    }
    
    if (event.target === bulkConfirmModal) {
        closeBulkConfirmModal();
    }
    

    if (event.target === stockModal) {
        closeStockModal();
    }
    if (event.target === deleteModal) {
        closeDeleteModal();
    }
}

// Tutup modal dengan tombol Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeStockModal();
        closeDeleteModal();
        closeBulkConfirmModal();
        closeEditModal();
    }
});


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
        
        reportContent.innerHTML = report.map(item => `
            <div class="report-card">
                <div class="report-item-header">
                    <div>
                        <div style="color: #999; font-size: 0.85em;">MID: ${item.mid}</div>
                        <div style="font-size: 1.2em; font-weight: 600; color: #333;">${item.name}</div>
                        <div style="color: #666; font-size: 0.9em;">Satuan: ${item.unit}</div>
                        <div style="color: #666; font-size: 0.9em;">Lokasi: ${item.storage_location || 'Belum ditentukan'}</div>
                    </div>
                    <div class="report-summary">
                        <div class="summary-box added">
                            <span class="summary-label">Ditambahkan</span>
                            <span class="summary-value">+${item.total_added}</span>
                        </div>
                        <div class="summary-box used">
                            <span class="summary-label">Digunakan</span>
                            <span class="summary-value">-${item.total_used}</span>
                        </div>
                    </div>
                </div>
                ${item.transactions.length > 0 ? `
                    <div class="transactions-list">
                        <table class="transactions-table">
                            <thead>
                                <tr>
                                    <th>Tanggal</th>
                                    <th>Tipe</th>
                                    <th>Jumlah</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${item.transactions.map(trans => {
                                    const date = new Date(trans.date);
                                    const formattedDate = date.toLocaleDateString('id-ID', {
                                        year: 'numeric',
                                        month: '2-digit',
                                        day: '2-digit'
                                    });
                                    const typeLabel = trans.type === 'in' ? 'Reservasi' : 'Digunakan';
                                    const typeStyle = trans.type === 'in' ? 'color: #48bb78; font-weight: 600;' : 'color: #f56565; font-weight: 600;';
                                    const quantityStyle = trans.type === 'in' ? 'color: #48bb78; font-weight: 600;' : 'color: #f56565; font-weight: 600;';
                                    const quantitySign = trans.type === 'in' ? '+' : '-';

                                    return `
                                        <tr>
                                            <td>${formattedDate}</td>
                                            <td style="${typeStyle}">${typeLabel}</td>
                                            <td style="${quantityStyle}">${quantitySign}${trans.quantity}</td>
                                        </tr>
                                    `;
                                }).join('')}
                            </tbody>
                        </table>
                    </div>
                ` : '<div style="color: #999; padding: 10px;">Tidak ada transaksi di bulan ini</div>'}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading report:', error);
        alert('Gagal memuat laporan');
    }
}

//sub menu
function showSubTab(subTabName) {
    // Sembunyikan semua sub-tab
    document.querySelectorAll('.sub-tab-content').forEach(tab => tab.classList.remove('active'));
    // Nonaktifkan semua tombol sub-tab
    document.querySelectorAll('.sub-tab-button').forEach(btn => btn.classList.remove('active'));
    // Tampilkan sub-tab yang dipilih
    document.getElementById(subTabName).classList.add('active');
    event.target.classList.add('active');
}

// ===== BULK RESERVATION FUNCTIONS =====

// Array untuk menyimpan daftar item ATK (untuk dropdown)
let availableItems = [];

// Load items saat halaman dimuat dan populate dropdown
async function loadAvailableItems() {
    try {
        const response = await fetch('/api/items');
        availableItems = await response.json();
        
        // Tambah baris pertama jika belum ada
        if (document.getElementById('reservationItemsContainer').children.length === 0) {
            addReservationRow();
        }
    } catch (error) {
        console.error('Error loading items:', error);
    }
}

// Fungsi untuk menambah baris reservasi baru
function addReservationRow() {
    const container = document.getElementById('reservationItemsContainer');
    const rowId = 'row-' + Date.now();
    
    const row = document.createElement('div');
    row.className = 'reservation-row';
    row.id = rowId;
    
    row.innerHTML = `
        <div class="row-number">${container.children.length + 1}</div>
        <select class="item-select" required>
            <option value="">-- Pilih Item --</option>
            ${availableItems.map(item => `
                <option value="${item.id}" data-unit="${item.unit}">
                    ${item.mid} - ${item.name} (Stock: ${item.stock} ${item.unit})
                </option>
            `).join('')}
        </select>
        <input type="number" class="quantity-input" placeholder="Jumlah" min="1" required>
        <span class="unit-display">-</span>
        <button type="button" onclick="removeReservationRow('${rowId}')" class="btn-remove-row">
            🗑️
        </button>
    `;
    
    container.appendChild(row);
    
    // Event listener untuk update unit display saat item dipilih
    const select = row.querySelector('.item-select');
    const unitDisplay = row.querySelector('.unit-display');
    
    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const unit = selectedOption.getAttribute('data-unit') || '-';
        unitDisplay.textContent = unit;
    });
    
    updateRowNumbers();
}

// Fungsi untuk menghapus baris reservasi
function removeReservationRow(rowId) {
    const row = document.getElementById(rowId);
    if (row) {
        row.remove();
        updateRowNumbers();
    }
}

// Update nomor urut baris
function updateRowNumbers() {
    const rows = document.querySelectorAll('.reservation-row');
    rows.forEach((row, index) => {
        const numberEl = row.querySelector('.row-number');
        if (numberEl) {
            numberEl.textContent = index + 1;
        }
    });
}

// Submit bulk reservation
// Data sementara untuk konfirmasi
let pendingBulkData = null;

// Validasi dan tampilkan modal konfirmasi
function submitBulkReservation() {
    const date = document.getElementById('bulkReservationDate').value;
    
    if (!date) {
        alert('Tanggal harus diisi!');
        return;
    }
    
    const rows = document.querySelectorAll('.reservation-row');
    
    if (rows.length === 0) {
        alert('Belum ada item yang ditambahkan!');
        return;
    }
    
    const items = [];
    let hasError = false;
    
    rows.forEach((row, index) => {
        const select = row.querySelector('.item-select');
        const quantityInput = row.querySelector('.quantity-input');
        
        const itemId = select.value;
        const quantity = parseInt(quantityInput.value);
        const itemText = select.options[select.selectedIndex].text;
        
        if (!itemId) {
            alert(`Baris ${index + 1}: Pilih item terlebih dahulu`);
            hasError = true;
            return;
        }
        
        if (!quantity || quantity <= 0) {
            alert(`Baris ${index + 1}: Jumlah harus lebih dari 0`);
            hasError = true;
            return;
        }
        
        items.push({
            item_id: parseInt(itemId),
            quantity: quantity,
            display_name: itemText
        });
    });
    
    if (hasError) return;
    
    // Simpan data sementara
    pendingBulkData = {
        items: items,
        date: date
    };
    
    // Tampilkan modal konfirmasi
    showBulkConfirmModal(date, items);
}

// Tampilkan modal konfirmasi
function showBulkConfirmModal(date, items) {
    const dateObj = new Date(date);
    const formattedDate = dateObj.toLocaleDateString('id-ID', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    document.getElementById('confirmDate').textContent = formattedDate;
    
    const tbody = document.getElementById('confirmItemsList');
    tbody.innerHTML = items.map((item, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${item.display_name}</td>
            <td style="font-weight: 600; color: #48bb78;">+${item.quantity}</td>
        </tr>
    `).join('');
    
    document.getElementById('bulkConfirmModal').classList.add('show');
}

// Tutup modal konfirmasi
function closeBulkConfirmModal() {
    document.getElementById('bulkConfirmModal').classList.remove('show');
    pendingBulkData = null;
}

// Eksekusi bulk reservation setelah konfirmasi
async function executeBulkReservation() {
    if (!pendingBulkData) return;
    
    const dateObj = new Date(pendingBulkData.date);
    const isoDate = dateObj.toISOString();
    
    // Hapus display_name sebelum kirim ke server
    const itemsToSend = pendingBulkData.items.map(item => ({
        item_id: item.item_id,
        quantity: item.quantity
    }));
    
    try {
        const response = await fetch('/api/items/bulk_reservation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: itemsToSend,
                date: isoDate
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            let message = result.message + '\n\n';
            
            if (result.results.length > 0) {
                message += 'Detail:\n';
                result.results.forEach(r => {
                    message += `✅ ${r.name}: +${r.quantity} (Stock baru: ${r.new_stock})\n`;
                });
            }
            
            if (result.errors.length > 0) {
                message += '\n⚠️ Error:\n' + result.errors.join('\n');
            }
            
            alert(message);
            
            closeBulkConfirmModal();
            
            // Clear form
            document.getElementById('reservationItemsContainer').innerHTML = '';
            document.getElementById('bulkReservationDate').value = new Date().toISOString().slice(0, 10);
            
            // Reload items
            await loadAvailableItems();
            loadItems();
        } else {
            alert('Error: ' + (result.error || 'Gagal menyimpan reservasi'));
        }
        
    } catch (error) {
        console.error('Error submitting bulk reservation:', error);
        alert('Terjadi kesalahan saat menyimpan');
    }
}
// Panggil saat halaman dimuat
document.addEventListener('DOMContentLoaded', function() {
    loadItems();
    setDefaultMonth();
    loadAvailableItems(); // Load items untuk bulk reservation
    
    // Set default date untuk bulk reservation
    const today = new Date();
    document.getElementById('bulkReservationDate').value = today.toISOString().slice(0, 10);
    
    document.getElementById('addItemForm').addEventListener('submit', addItem);
});