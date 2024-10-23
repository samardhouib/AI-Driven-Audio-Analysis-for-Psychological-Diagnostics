from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class PDFGenerator:
    @staticmethod
    def generate_pdf(extracted_summary, output_filename):
        # Create the PDF document
        doc = SimpleDocTemplate(output_filename, pagesize=letter)

        # Create styles for the PDF
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name='Title', fontSize=18, spaceAfter=12, alignment=1)
        heading_style = ParagraphStyle(name='Heading', fontSize=14, spaceAfter=6, fontName='Helvetica-Bold')
        text_style = ParagraphStyle(name='Text', fontSize=12, spaceAfter=12)

        # Create content for the PDF
        content = []
        content.append(Paragraph("Medical Summary", title_style))

        for key, value in extracted_summary.items():
            content.append(Paragraph(key, heading_style))
            content.append(Paragraph(value, text_style))
            content.append(Spacer(1, 12))

        doc.build(content)
        print(f"PDF created at {output_filename}")
