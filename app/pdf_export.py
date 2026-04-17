"""
PDF Export for Grant-Ready Business Plan Writer.
Generates a clean, professional PDF document from a completed business plan.
Uses fpdf2 for PDF generation (no external dependencies like LaTeX).
"""
import io
import re
from fpdf import FPDF
from app.plan_builder import BusinessPlan
from app.prompts import SECTION_ORDER, SECTION_PROMPTS
class BusinessPlanPDF(FPDF):
 """Custom PDF class with headers and footers for the business plan."""
 def __init__(self, business_name: str):
 super().__init__()
 self.business_name = business_name
 def header(self):
 """Page header with business name."""
 self.set_font("Helvetica", "B", 9)
 self.set_text_color(120, 120, 120)
 self.cell(0, 10, self.business_name, align="L")
 self.cell(0, 10, "Business Plan", align="R", new_x="LMARGIN", new_y="NEXT")
 self.set_draw_color(200, 200, 200)
 self.line(10, self.get_y(), 200, self.get_y())
 self.ln(5)
 def footer(self):
 """Page footer with page number."""
 self.set_y(-15)
 self.set_font("Helvetica", "I", 8)
 self.set_text_color(150, 150, 150)
 self.cell(
 0,
 10,
 f"Page {self.page_no()}/{{nb}} | Grant-Ready Business Plan Writer",
 align="C",
 )
def _clean_text(text: str) -> str:
 """Remove markdown formatting and clean text for PDF."""
 # Remove markdown bold
 text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
 # Remove markdown italic
 text = re.sub(r"\*(.*?)\*", r"\1", text)
 # Remove markdown headers
 text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
 # Remove horizontal rules
 text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
 # Remove trailing approval questions from Llama
 for phrase in [
 "Does this look good",
 "Would you like me to change",
 "Shall I make any",
 "Let me know if",
 "Would you like to revise",
 ]:
 if phrase in text:
 text = text[: text.index(phrase)].rstrip("\n -—")
 return text.strip()
def generate_pdf(plan: BusinessPlan) -> bytes:
 """
 Generate a PDF document from a completed business plan.
 Args:
 plan: A BusinessPlan object with all sections.
 Returns:
 PDF file content as bytes.
 """
 pdf = BusinessPlanPDF(plan.business_name)
 pdf.alias_nb_pages()
 pdf.set_auto_page_break(auto=True, margin=20)
 pdf.add_page()
 # -- Title Page Content --
 pdf.ln(30)
 pdf.set_font("Helvetica", "B", 28)
 pdf.set_text_color(30, 30, 30)
 pdf.cell(0, 15, "Business Plan", align="C", new_x="LMARGIN", new_y="NEXT")
 pdf.ln(5)
 pdf.set_font("Helvetica", "", 18)
 pdf.set_text_color(60, 60, 60)
 pdf.cell(
 0, 12, plan.business_name, align="C", new_x="LMARGIN", new_y="NEXT"
 )
 pdf.ln(10)
 pdf.set_draw_color(50, 50, 50)
 pdf.line(70, pdf.get_y(), 140, pdf.get_y())
 pdf.ln(10)
 pdf.set_font("Helvetica", "I", 11)
 pdf.set_text_color(100, 100, 100)
 pdf.cell(
 0,
 8,
 "Prepared with Grant-Ready Business Plan Writer",
 align="C",
 new_x="LMARGIN",
 new_y="NEXT",
 )
 # -- Table of Contents --
 pdf.add_page()
 pdf.set_font("Helvetica", "B", 18)
 pdf.set_text_color(30, 30, 30)
 pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
 pdf.ln(5)
 for key in SECTION_ORDER:
 section_def = SECTION_PROMPTS[key]
 pdf.set_font("Helvetica", "", 12)
 pdf.set_text_color(60, 60, 60)
 label = f"{section_def['number']}. {section_def['name']}"
 status = "Complete" if plan.sections.get(key) else "Not Completed"
 pdf.cell(140, 8, label)
 pdf.set_font("Helvetica", "I", 10)
 pdf.set_text_color(140, 140, 140)
 pdf.cell(0, 8, status, align="R", new_x="LMARGIN", new_y="NEXT")
 # -- Section Pages --
 for key in SECTION_ORDER:
 section_def = SECTION_PROMPTS[key]
 pdf.add_page()
 # Section header
 pdf.set_font("Helvetica", "B", 8)
 pdf.set_text_color(100, 130, 200)
 pdf.cell(
 0,
 6,
 f"SECTION {section_def['number']} OF 8",
 new_x="LMARGIN",
 new_y="NEXT",
 )
 pdf.set_font("Helvetica", "B", 18)
 pdf.set_text_color(30, 30, 30)
 pdf.cell(
 0, 12, section_def["name"], new_x="LMARGIN", new_y="NEXT"
 )
 pdf.ln(3)
 pdf.set_draw_color(100, 130, 200)
 pdf.set_line_width(0.5)
 pdf.line(10, pdf.get_y(), 60, pdf.get_y())
 pdf.set_line_width(0.2)
 pdf.ln(8)
 # Section content
 content = plan.sections.get(key, "")
 if content:
 cleaned = _clean_text(content)
 pdf.set_font("Helvetica", "", 11)
 pdf.set_text_color(50, 50, 50)
 for paragraph in cleaned.split("\n\n"):
 paragraph = paragraph.strip()
 if paragraph:
 pdf.multi_cell(0, 6, paragraph)
 pdf.ln(4)
 else:
 pdf.set_font("Helvetica", "I", 11)
 pdf.set_text_color(150, 150, 150)
 pdf.cell(0, 8, "This section was not completed.")
 # -- Output --
 return pdf.output()
