"""
Plan Builder for Grant-Ready Business Plan Writer.
Assembles the completed sections into a structured business plan document.
"""
from dataclasses import dataclass
from app.prompts import SECTION_ORDER, SECTION_PROMPTS
from app.conversation import ConversationState
@dataclass
class BusinessPlan:
 """A completed business plan ready for export."""
 business_name: str
 sections: dict[str, str] # section_key -> refined_text
 def to_plain_text(self) -> str:
 """Export the plan as formatted plain text."""
 lines = []
 lines.append("=" * 60)
 lines.append(f"BUSINESS PLAN: {self.business_name.upper()}")
 lines.append("=" * 60)
 lines.append("")
 lines.append(f"Prepared with Grant-Ready Business Plan Writer")
 lines.append("")
 for key in SECTION_ORDER:
 section_def = SECTION_PROMPTS[key]
 lines.append("-" * 60)
 lines.append(
 f"SECTION {section_def['number']}: "
 f"{section_def['name'].upper()}"
 )
 lines.append("-" * 60)
 lines.append("")
 if key in self.sections and self.sections[key]:
 lines.append(self.sections[key])
 else:
 lines.append("[This section was not completed]")
 lines.append("")
 lines.append("")
 lines.append("=" * 60)
 lines.append("END OF BUSINESS PLAN")
 lines.append("=" * 60)
 return "\n".join(lines)
 def to_markdown(self) -> str:
 """Export the plan as Markdown."""
 lines = []
 lines.append(f"# Business Plan: {self.business_name}")
 lines.append("")
 lines.append("*Prepared with Grant-Ready Business Plan Writer*")
 lines.append("")
 lines.append("---")
 lines.append("")
 for key in SECTION_ORDER:
 section_def = SECTION_PROMPTS[key]
 lines.append(
 f"## {section_def['number']}. {section_def['name']}"
 )
 lines.append("")
 if key in self.sections and self.sections[key]:
 # Clean up the refined text (remove any approval questions)
 text = self.sections[key]
 # Remove common trailing questions from Llama
 for phrase in [
 "Does this look good",
 "Would you like me to change",
 "Shall I make any",
 "Let me know if",
 "Would you like to revise",
 ]:
 if phrase in text:
 text = text[: text.index(phrase)].rstrip("\n -—")
 lines.append(text.strip())
 else:
 lines.append("*This section was not completed.*")
 lines.append("")
 lines.append("---")
 lines.append("")
 return "\n".join(lines)
def build_plan(state: ConversationState) -> BusinessPlan:
 """
 Build a BusinessPlan from a completed ConversationState.
 Args:
 state: The conversation state with completed sections.
 Returns:
 A BusinessPlan object ready for export.
 """
 sections = {}
 for key in SECTION_ORDER:
 section_state = state.sections[key]
 if section_state.approved and section_state.refined_text:
 sections[key] = section_state.refined_text
 else:
 sections[key] = ""
 return BusinessPlan(
 business_name=state.business_name,
 sections=sections,
 )
