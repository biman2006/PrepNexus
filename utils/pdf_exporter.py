import os
import html
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


def escape_xml(text: str) -> str:
    """
    Safely escape plain text for ReportLab XML flowables.
    """
    if not text:
        return ""
    # Unescape first to avoid double-escaping if already escaped
    raw = html.unescape(str(text))
    return html.escape(raw)


def generate_resume_pdf(
    resume_text: str,
    output_path: str = "generated_resumes/PrepNexus_Resume.pdf",
    template: str = "modern"
) -> str:
    """
    Converts resume text into a polished, production-ready PDF.
    
    Templates available:
    - 'modern': Modern Clean design with indigo accent headers and clean divider bars.
    - 'classic': Executive Classic monochrome corporate styling with formal serif/sans headers.
    - 'minimalist': Clean ATS Minimalist high-readability layout for legacy ATS parsers.
    """
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Document setup with 0.5-inch margins
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Determine color palette based on template
    if template == "modern":
        accent_color = colors.HexColor("#2563EB")
        name_color = colors.HexColor("#0F172A")
        header_bar_color = colors.HexColor("#E2E8F0")
    elif template == "classic":
        accent_color = colors.HexColor("#1E293B")
        name_color = colors.HexColor("#000000")
        header_bar_color = colors.HexColor("#94A3B8")
    else:  # minimalist
        accent_color = colors.HexColor("#000000")
        name_color = colors.HexColor("#000000")
        header_bar_color = colors.HexColor("#CBD5E1")

    # Custom paragraph styles
    name_style = ParagraphStyle(
        "CustomResumeName",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=name_color,
        alignment=0,
        spaceAfter=3,
    )

    contact_style = ParagraphStyle(
        "CustomResumeContact",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
        alignment=0,
        spaceAfter=8,
    )

    section_heading_style = ParagraphStyle(
        "CustomResumeHeading",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "CustomResumeBody",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=3,
    )

    bullet_style = ParagraphStyle(
        "CustomResumeBullet",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        spaceAfter=2,
    )

    subheading_style = ParagraphStyle(
        "CustomResumeSubheading",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True,
    )

    story = []
    lines = [line.strip() for line in resume_text.split("\n")]

    first_non_empty = True
    in_contact_block = False

    for idx, raw_line in enumerate(lines):
        if not raw_line:
            story.append(Spacer(1, 3))
            continue

        clean = escape_xml(raw_line)

        # Header Name (First line)
        if first_non_empty:
            story.append(Paragraph(clean, name_style))
            first_non_empty = False
            in_contact_block = True
            continue

        # Contact info line
        if in_contact_block and ("email" in raw_line.lower() or "phone" in raw_line.lower() or "linkedin" in raw_line.lower() or "github" in raw_line.lower()):
            story.append(Paragraph(clean, contact_style))
            if template != "minimalist":
                story.append(HRFlowable(width="100%", thickness=1, color=header_bar_color, spaceBefore=2, spaceAfter=8))
            in_contact_block = False
            continue
        else:
            in_contact_block = False

        # Section Headings (ALL CAPS or ending with :)
        is_heading = (raw_line.isupper() and len(raw_line) > 2) or (raw_line.endswith(":") and not raw_line.startswith("-") and not raw_line.startswith("•"))
        
        if is_heading:
            clean_title = clean.rstrip(":")
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>{clean_title.upper()}</b>", section_heading_style))
            story.append(HRFlowable(width="100%", thickness=0.8, color=header_bar_color, spaceBefore=1, spaceAfter=5))

        # Bullet point line
        elif raw_line.startswith("-") or raw_line.startswith("•") or raw_line.startswith("*"):
            bullet_content = clean.lstrip("-•* ").strip()
            # Highlight leading bold text if it has a colon like "Languages: Python, Java"
            if ":" in bullet_content:
                parts = bullet_content.split(":", 1)
                formatted_bullet = f"<b>{parts[0].strip()}:</b> {parts[1].strip()}"
            else:
                formatted_bullet = bullet_content

            story.append(Paragraph(f"&bull; {formatted_bullet}", bullet_style))

        # Role / Company / Project subheadings
        elif ("|" in raw_line or " - " in raw_line) and len(raw_line) < 120 and not raw_line.startswith("Target Role:"):
            story.append(Paragraph(f"<b>{clean}</b>", subheading_style))

        # Normal text line (e.g. summary or target role)
        else:
            if clean.startswith("Target Role:"):
                story.append(Paragraph(f"<b>{clean}</b>", subheading_style))
            else:
                story.append(Paragraph(clean, body_style))

    doc.build(story)
    return output_path