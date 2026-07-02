"""
Generador de comprobantes PDF para USICAMM
"""

import logging
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from config import TEMP_DIR, LOG_FILE

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(LOG_FILE)])
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generador de PDFs"""

    def __init__(self):
        self.temp_dir = TEMP_DIR
        self.temp_dir.mkdir(exist_ok=True)

    def generar_pdf_conclusion(self, resultado: dict) -> str:
        """
        Generar PDF de conclusión del examen

        Args:
            resultado: Diccionario con resultados del examen

        Returns:
            Ruta del archivo PDF generado
        """
        try:
            # Crear nombre del archivo
            curp = resultado.get('curp', 'DESCONOCIDO')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Comprobante_USICAMM_{curp}_{timestamp}.pdf"
            ruta_pdf = self.temp_dir / nombre_archivo

            # Crear documento
            doc = SimpleDocTemplate(
                str(ruta_pdf),
                pagesize=letter,
                rightMargin=0.5 * inch,
                leftMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch
            )

            # Estilos
            styles = getSampleStyleSheet()
            titulo_style = ParagraphStyle(
                'Titulo',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1E40AF'),
                spaceAfter=12,
                alignment=1  # Centro
            )

            # Contenido
            elementos = []

            # Título
            elementos.append(
                Paragraph(
                    "COMPROBANTE DE CONCLUSIÓN DE EXAMEN",
                    titulo_style
                )
            )
            elementos.append(
                Paragraph("USICAMM", styles['Normal'])
            )
            elementos.append(Spacer(1, 0.2 * inch))

            # Datos del aspirante
            datos_aspirante = [
                ["CURP:", resultado.get('curp', 'N/A')],
                ["Nombre:", resultado.get('nombre_aspirante', 'N/A')],
                ["Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ]

            tabla_aspirante = Table(datos_aspirante)
            tabla_aspirante.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1E40AF')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elementos.append(tabla_aspirante)
            elementos.append(Spacer(1, 0.3 * inch))

            # Resultados
            elementos.append(
                Paragraph("RESULTADOS DEL EXAMEN", styles['Heading2'])
            )
            elementos.append(Spacer(1, 0.1 * inch))

            resultados_data = [
                ["Puntuación:", f"{resultado.get('puntuacion', 0)}/100"],
                ["Porcentaje de Acierto:", f"{resultado.get('porcentaje_acierto', 0):.1f}%"],
                ["Preguntas Respondidas:", str(resultado.get('preguntas_respondidas', 0))],
                ["Preguntas Correctas:", f"{resultado.get('preguntas_correctas', 0)}/{resultado.get('preguntas_totales', 0)}"],
            ]

            tabla_resultados = Table(resultados_data)
            tabla_resultados.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))

            elementos.append(tabla_resultados)
            elementos.append(Spacer(1, 0.3 * inch))

            # Pie de página
            elementos.append(
                Paragraph(
                    "Este comprobante certifica la conclusión del examen de evaluación en USICAMM.",
                    styles['Normal']
                )
            )

            # Generar PDF
            doc.build(elementos)

            logger.info(f"✅ PDF generado: {ruta_pdf}")
            return str(ruta_pdf)

        except Exception as e:
            logger.error(f"❌ Error al generar PDF: {e}")
            return ""
