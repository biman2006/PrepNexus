import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_resume_pdf(
    resume_text,
    output_path="generated_resumes/PrepNexus_Resume.pdf"
):
    """
    Converts generated resume text into a professional PDF.

    Parameters:
    - resume_text: Full generated resume string from API
    - output_path: PDF save location

    Returns:
    - output_path
    """

    # ==========================================
    # CREATE OUTPUT FOLDER IF NOT EXISTS
    # ==========================================
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    # ==========================================
    # PDF SETUP
    # ==========================================
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        spaceAfter=4,
        spaceBefore=0,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading4"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        spaceAfter=6,
        spaceBefore=6,
    )

    story = []

    # ==========================================
    # SPLIT TEXT
    # ==========================================
    lines = resume_text.split("\n")

    # ==========================================
    # BUILD CONTENT
    # ==========================================
    for line in lines:

        line = line.strip()

        # Empty lines
        if not line:
            story.append(Spacer(1, 0.08 * inch))
            continue

        # Headings
        if line.isupper() or line.endswith(":"):
            story.append(Paragraph(f"<b>{line}</b>", heading_style))

        # Bullet points
        elif line.startswith("-"):
            story.append(Paragraph(f"• {line[1:].strip()}", body_style))

        # Normal text
        else:
            story.append(Paragraph(line, body_style))

        story.append(Spacer(1, 0.05 * inch))

    # ==========================================
    # BUILD PDF
    # ==========================================
    doc.build(story)

    return output_path