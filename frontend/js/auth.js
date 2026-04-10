const API_URL = "";
console.log("AUTH JS CARGADO");
// LOGIN
document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) return;

    loginForm.addEventListener("submit", async function (e) {

    console.log("SUBMIT DETECTADO");
    e.preventDefault();

    const usuario = document.getElementById("dni").value.trim();
    const password = document.getElementById("password").value;

    console.log("Datos:", usuario, password);

    try {

        console.log("ANTES DEL FETCH");

      await fetch("/auth/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    credentials: "include", 
    body: JSON.stringify({
        dni: usuario,
        password: password
    })
});

        console.log("DESPUÉS DEL FETCH");

        const data = await response.json();

        console.log("DATA:", data);

        if (!response.ok) {
            console.log("ERROR BACKEND");
            alert(data.detail || "Error de login");
            return;
        }

        alert("LOGIN OK");

        const user = data.usuario;

        console.log("ROL:", user.rol);

        if (user.rol === "admin") {
            alert("REDIRIGIENDO ADMIN");
            window.location.href = "/admin/dashAdmin.html";
        } else if (user.rol === "preceptor") {
            alert("REDIRIGIENDO PRECEPTOR");
            window.location.href = "/preceptor/dash.html";
        } else if (user.rol === "alumno") {
            alert("REDIRIGIENDO ALUMNO");
            window.location.href = "/alumno/dashboard.html";
        } else {
            alert("ROL DESCONOCIDO");
        }

    } catch (error) {
        console.error("ERROR REAL:", error);
        alert("Error de conexión");
    }

});

});
