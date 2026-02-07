// ===== DASHBOARD FUNCTIONS =====

// Load dashboard saat halaman dimuat
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

// Load dashboard data
async function loadDashboard() {
    try {
        const response = await fetch('/api/dashboard/storage');
        
        if (!response.ok) {
            throw new Error('Gagal memuat data dashboard');
        }
        
        const storageData = await response.json();
        renderDashboard(storageData);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Gagal memuat dashboard', 'error');
    }
}

// Render dashboard cards
function renderDashboard(storageData) {
    const dashboardContent = document.getElementById('dashboardContent');
    
    if (storageData.length === 0) {
        dashboardContent.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">Belum ada data item.</p>';
        return;
    }
    
    dashboardContent.innerHTML = storageData.map(storage => {
        const previewItems = storage.items.slice(0, 5);
        const hasMore = storage.items.length > 5;
        
        return `
            <div class="dashboard-card">
                <div class="dashboard-card-header">
                    <h3>🗃️ ${storage.location}</h3>
                    <div class="dashboard-stats">
                        <span class="stat-badge total">${storage.total_items} Item</span>
                        ${storage.empty_stock_count > 0 ? `<span class="stat-badge empty">${storage.empty_stock_count} Habis</span>` : ''}
                        ${storage.low_stock_count > 0 ? `<span class="stat-badge low">${storage.low_stock_count} Rendah</span>` : ''}
                    </div>
                </div>
                <div class="dashboard-card-body">
                    <div class="items-preview">
                        ${previewItems.map(item => {
                            let stockClass = '';
                            let stockLabel = '';
                            
                            if (item.stock === 0) {
                                stockClass = 'empty';
                                stockLabel = 'HABIS';
                            } else if (item.stock < 10) {
                                stockClass = 'low';
                                stockLabel = 'RENDAH';
                            } else if (item.stock <= 50) {
                                stockClass = 'medium';
                                stockLabel = 'SEDANG';
                            } else {
                                stockClass = 'high';
                                stockLabel = 'TINGGI';
                            }
                            
                            return `
                                <div class="item-preview">
                                    <div class="item-preview-info">
                                        <span class="item-preview-mid">${item.mid}</span>
                                        <span class="item-preview-name">${item.name}</span>
                                    </div>
                                    <div class="item-preview-stock ${stockClass}">
                                        <span class="stock-value">${item.stock} ${item.unit}</span>
                                        <span class="stock-status">${stockLabel}</span>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                    ${hasMore ? `
                        <button class="btn-show-all" onclick='showAllItems(${JSON.stringify(storage)})'>
                            Lihat Semua (${storage.items.length} item)
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Show all items modal
function showAllItems(storage) {
    const modalHTML = `
        <div id="allItemsModal" class="modal show">
            <div class="modal-content modal-large">
                <div class="modal-header">
                    <h2>🗃️ ${storage.location} - Semua Item (${storage.items.length})</h2>
                    <span class="close" onclick="closeAllItemsModal()">&times;</span>
                </div>
                <div class="modal-body">
                    <table class="items-detail-table">
                        <thead>
                            <tr>
                                <th>No</th>
                                <th>MID</th>
                                <th>Nama Item</th>
                                <th>Stok</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${storage.items.map((item, index) => {
                                let stockClass = '';
                                let stockLabel = '';
                                
                                if (item.stock === 0) {
                                    stockClass = 'empty';
                                    stockLabel = 'HABIS';
                                } else if (item.stock < 10) {
                                    stockClass = 'low';
                                    stockLabel = 'RENDAH';
                                } else if (item.stock <= 50) {
                                    stockClass = 'medium';
                                    stockLabel = 'SEDANG';
                                } else {
                                    stockClass = 'high';
                                    stockLabel = 'TINGGI';
                                }
                                
                                return `
                                    <tr>
                                        <td>${index + 1}</td>
                                        <td>${item.mid}</td>
                                        <td>${item.name}</td>
                                        <td><strong>${item.stock} ${item.unit}</strong></td>
                                        <td><span class="stock-badge ${stockClass}">${stockLabel}</span></td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
                <div class="modal-footer">
                    <button onclick="closeAllItemsModal()" class="btn-cancel">Tutup</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function closeAllItemsModal() {
    const modal = document.getElementById('allItemsModal');
    if (modal) {
        modal.remove();
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('allItemsModal');
    if (event.target === modal) {
        closeAllItemsModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAllItemsModal();
    }
});