document.addEventListener("DOMContentLoaded", async () => {

    try {

        const response = await fetch("/alumnos/mi-boleta", {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            console.log("No autorizado → redirigiendo al login");
            window.location.href = "/login.html";
            return;
        }

        const data = await response.json();

        console.log("DATA BOLETA:", data);

        // =========================
        // DATOS DEL ALUMNO
        // =========================

        document.getElementById("nombreUsuario").textContent = data.alumno;
        document.getElementById("nombreAlumno").textContent = data.alumno;

        // =========================
        // TABLA DE NOTAS
        // =========================

        const tabla = document.getElementById("tablaNotas");
        tabla.innerHTML = "";

        data.materias.forEach(m => {

            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${m.materia}</td>
                <td>${m.notas[0] ?? "-"}</td>
                <td>${m.notas[1] ?? "-"}</td>
                <td>${m.notas[2] ?? "-"}</td>
                <td>${m.promedio}</td>
                <td>${m.estado}</td>
            `;

            tabla.appendChild(fila);
        });

        // =========================
        // PROMEDIO GENERAL
        // =========================

        document.getElementById("promedioGeneral").textContent = data.promedio_general;

    } catch (error) {
        console.error("Error:", error);
    }

});