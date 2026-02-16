from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def generate_pdf(filename, topic, cosine_score, draft_text, reference):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(
        f"<b>Research Paper Draft</b><br/>{topic}",
        styles["Title"]
    ))
    story.append(Spacer(1, 12))

    # Cosine similarity
    story.append(Paragraph(
        f"<b>Cosine Similarity Score:</b> {cosine_score}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 12))

    # Draft content
    story.append(Paragraph("<b>Generated Draft</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    for line in draft_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))

    # Reference
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Reference (APA)</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(reference, styles["Normal"]))

    doc.build(story)
