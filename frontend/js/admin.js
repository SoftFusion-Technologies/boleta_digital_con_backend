document.addEventListener("DOMContentLoaded", async () => {

    const user = await getUsuarioActual();

    if (!user || user.rol !== "admin") {
        window.location.href = "/login.html";
    }

});

// CREAR USUARIO
async function crearUsuario() {

    const nombre = prompt("Nombre:");
    const usuario = prompt("DNI o username:");
    const password = prompt("Contraseña:");
    const rol = prompt("Rol (admin/preceptor/alumno):");

    if (!nombre || !usuario || !password || !rol) {
        alert("Datos incompletos");
        return;
    }

    try {

        const response = await apiFetch("/usuarios", {
            method: "POST",
            body: JSON.stringify({
                nombre,
                usuario,
                password,
                rol
            })
        });

        if (!response.ok) {
            alert("Error al crear usuario");
            return;
        }

        alert("Usuario creado");

    } catch (error) {
        console.error(error);
        alert("Error");
    }
}