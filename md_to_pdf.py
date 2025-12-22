import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def parse_markdown_to_pdf(md_file_path, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='CodeBlock', fontName='Courier', fontSize=8, leading=10, backColor=colors.lightgrey, spaceAfter=10, leftIndent=10))
    # Use a unique name for bullet style or update existing if possible, but adding new is safer
    styles.add(ParagraphStyle(name='MyBullet', parent=styles['BodyText'], bulletIndent=10, leftIndent=20, spaceAfter=5))
    
    story = []
    
    # Title Page Idea or just Title at top
    story.append(Paragraph("Project Concepts Report: Aryal Agro ERP", styles['Title']))
    story.append(Spacer(1, 24))
    
    try:
        with open(md_file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find file {md_file_path}")
        return

    in_code_block = False
    code_block_content = []
    
    for line in lines:
        line = line.rstrip()
        
        # Skip top level title if it matches my manual title
        if line.startswith('# Project Concepts Report'):
            continue
            
        # Handle Code Blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of block
                p = Preformatted('\n'.join(code_block_content), styles['CodeBlock'])
                story.append(p)
                code_block_content = []
                in_code_block = False
            else:
                # Start of block
                in_code_block = True
            continue
            
        if in_code_block:
            code_block_content.append(line)
            continue
            
        # Handle Headings
        if line.startswith('# '):
            story.append(Paragraph(line[2:], styles['Title']))
            story.append(Spacer(1, 12))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['Heading2']))
            story.append(Spacer(1, 10))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['Heading3']))
            story.append(Spacer(1, 8))
            
        # Handle Bullets
        elif line.strip().startswith('* ') or line.strip().startswith('- '):
            text = line.strip()[2:]
            # Simple bold parsing
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(f'&bull; {text}', styles['MyBullet']))
            
        # Handle Normal Text
        elif line.strip():
            text = line
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            story.append(Paragraph(text, styles['BodyText']))
            story.append(Spacer(1, 6))
            
    doc.build(story)
    print(f"PDF generated at: {output_pdf_path}")

if __name__ == "__main__":
    md_path = "/Users/badalaryal/.gemini/antigravity/brain/24a76b53-f350-46c1-b15e-9e20a65a7824/project_concepts_report.md"
    pdf_path = "/Users/badalaryal/.gemini/antigravity/brain/24a76b53-f350-46c1-b15e-9e20a65a7824/project_concepts_report.pdf"
    parse_markdown_to_pdf(md_path, pdf_path)
