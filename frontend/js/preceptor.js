document.addEventListener("DOMContentLoaded", async () => {

    const user = await getUsuarioActual();

    if (!user || user.rol !== "preceptor") {
        window.location.href = "/login.html";
    }

});

// GUARDAR NOTAS
async function saveGrades() {

    const filas = document.querySelectorAll('tbody tr');
    const notas = [];

    filas.forEach(fila => {

        const materia = fila.querySelector('td').textContent;

        fila.querySelectorAll('.grade-input').forEach((input, index) => {

            const valor = parseFloat(input.value);

            if (!isNaN(valor)) {
                notas.push({
                    materia,
                    trimestre: index + 1,
                    nota: valor
                });
            }

        });

    });

    try {

        const response = await apiFetch("/notas", {
            method: "POST",
            body: JSON.stringify(notas)
        });

        if (!response.ok) {
            alert("Error al guardar");
            return;
        }

        alert("Notas guardadas");

    } catch (error) {
        console.error(error);
    }

}