from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf_report(report: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle("Body", parent=styles["BodyText"], leading=14, fontSize=10)
    title_style = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=20, textColor=colors.HexColor("#111827"))

    elements = []
    elements.append(Paragraph("AI SEO Audit Report", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"URL: {report.get('url', '-')}", body_style))
    elements.append(Paragraph(f"SEO Score: {report.get('seo_score', '-')}", body_style))
    elements.append(Spacer(1, 0.2 * inch))

    breakdown = report.get("audit_breakdown", {})
    table_data = [["Category", "Score"]]
    for key in ["keyword_density", "meta_tags", "heading_structure", "internal_linking"]:
        table_data.append([key.replace("_", " ").title(), f"{breakdown.get(key, 0)}"])

    table = Table(table_data, colWidths=[3.8 * inch, 1.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FAFB")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 0.25 * inch))

    elements.append(Paragraph("Top Suggestions", styles["Heading3"]))
    for suggestion in report.get("suggestions", [])[:12]:
        elements.append(Paragraph(f"- {suggestion}", body_style))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

