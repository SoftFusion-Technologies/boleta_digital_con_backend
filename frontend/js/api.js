const API_URL = "";

// Función helper para fetch con token
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login.html";
        return;
    }

    return response;
}