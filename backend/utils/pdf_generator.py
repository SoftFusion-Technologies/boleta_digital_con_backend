from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generar_boleta_pdf(nombre_alumno, datos):

    doc = SimpleDocTemplate("boleta.pdf")
    styles = getSampleStyleSheet()

    elementos = []

    titulo = Paragraph(f"Boleta de Calificaciones - {nombre_alumno}", styles["Title"])
    elementos.append(titulo)

    tabla_data = [["Materia", "Promedio", "Estado"]]

    for m in datos["materias"]:
        tabla_data.append([
            m["materia"],
            str(m["promedio"]),
            m["estado"]
        ])

    tabla = Table(tabla_data)

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black)
    ]))

    elementos.append(tabla)

    elementos.append(Paragraph(
        f"Promedio General: {datos['promedio_general']}",
        styles["Heading2"]
    ))

    doc.build(elementos)

    return "boleta.pdf"