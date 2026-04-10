// Función para cerrar sesión
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        // Aquí iría la llamada al backend para cerrar sesión
        window.location.href = '../login.html';
    }
}

// Función para mostrar mensaje de éxito
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message fade-in';
    successDiv.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.709 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13418 4.39828 5.4928C5.79935 3.85141 7.70276 2.69537 9.86666 2.17117C12.0306 1.64698 14.3605 1.77744 16.58 2.547L19 5M15 10L19 6M22 9V5H18" stroke="white" stroke-width="2"/>
        </svg>
        <span>${message}</span>
    `;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Función para mostrar mensaje de error
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message fade-in';
    errorDiv.style.display = 'block';
    errorDiv.style.position = 'fixed';
    errorDiv.style.top = '20px';
    errorDiv.style.right = '20px';
    errorDiv.style.zIndex = '10000';
    errorDiv.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="vertical-align: middle;">
            <path d="M12 9V11M12 15H12.01M10.83 20.28L3.76 18.16C2.7 17.84 2 16.89 2 15.76V8.24C2 7.11 2.7 6.16 3.76 5.84L10.83 3.72C11.58 3.49 12.42 3.49 13.17 3.72L20.24 5.84C21.3 6.16 22 7.11 22 8.24V15.76C22 16.89 21.3 17.84 20.24 18.16L13.17 20.28C12.42 20.51 11.58 20.51 10.83 20.28Z" stroke="currentColor" stroke-width="2"/>
        </svg>
        <span style="vertical-align: middle; margin-left: 8px;">${message}</span>
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Función para formatear fecha
function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
}

// Función para formatear hora
function formatTime(date) {
    const d = new Date(date);
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

// ========================================
// FUNCIONES DE CARGA
// ========================================

// Mostrar loading
function showLoading() {
    const loading = document.createElement('div');
    loading.id = 'loadingOverlay';
    loading.style.position = 'fixed';
    loading.style.top = '0';
    loading.style.left = '0';
    loading.style.width = '100%';
    loading.style.height = '100%';
    loading.style.background = 'rgba(255, 255, 255, 0.8)';
    loading.style.display = 'flex';
    loading.style.justifyContent = 'center';
    loading.style.alignItems = 'center';
    loading.style.zIndex = '9999';
    loading.innerHTML = `
        <div class="spinner"></div>
    `;
    document.body.appendChild(loading);
}

// Ocultar loading
function hideLoading() {
    const loading = document.getElementById('loadingOverlay');
    if (loading) {
        loading.remove();
    }
}

// FUNCIONES DE VALIDACIÓN

// Validar DNI
function validateDNI(dni) {
    const dniRegex = /^\d{7,8}$/;
    return dniRegex.test(dni);
}

// Validar email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validar contraseña
function validatePassword(password) {
    return password.length >= 6;
}


// FUNCIONES DE EXPORTACIÓN (Simuladas)


// Exportar a PDF
function exportPDF() {
    showLoading();
    setTimeout(() => {
        hideLoading();
        showSuccess(' Boleta exportada a PDF correctamente');
        // Aquí iría la llamada real al backend
        console.log('Exportando a PDF...');
    }, 1000);
}

// Exportar a Excel
function exportExcel() {
    showLoading();
    setTimeout(() => {
        hideLoading();
        showSuccess('Boleta exportada a Excel correctamente');
        // Aquí iría la llamada real al backend
        console.log('Exportando a Excel...');
    }, 1000);
}


// INICIALIZACIÓN

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de Boletas Digitales cargado');
    
    // Agregar eventos a botones con clases específicas
    document.querySelectorAll('.btn-logout').forEach(btn => {
        btn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
                // Aquí iría la llamada al backend
                window.location.href = 'login.html';
            }
        });
    });
});