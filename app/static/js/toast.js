// ===== TOAST NOTIFICATION SYSTEM =====

function showToast(message, type = 'info', duration = 10000) {
    // Buat container jika belum ada
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Icon berdasarkan type
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    // Titles berdasarkan type
    const titles = {
        success: 'Berhasil',
        error: 'Error',
        warning: 'Peringatan',
        info: 'Informasi'
    };
    
    // Buat toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-content">
            <div class="toast-title">${titles[type] || titles.info}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="closeToast(this)">×</button>
        <div class="toast-progress"></div>
    `;
    
    container.appendChild(toast);
    
    // Auto remove setelah duration
    setTimeout(() => {
        removeToast(toast);
    }, duration);
}

function closeToast(button) {
    const toast = button.closest('.toast');
    removeToast(toast);
}

function removeToast(toast) {
    toast.classList.add('removing');
    setTimeout(() => {
        toast.remove();
        
        // Hapus container jika kosong
        const container = document.querySelector('.toast-container');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 300);
}

