"""
Conversation State Machine for Grant-Ready Business Plan Writer.
Manages the flow through 8 business plan sections, tracking where the
user is in the process and what information has been collected.
"""
from dataclasses import dataclass, field
from enum import Enum
from app.prompts import SECTION_ORDER, SECTION_PROMPTS, SYSTEM_PROMPT
from app.llm_engine import engine
class Phase(str, Enum):
 """Phases within each section."""
 INTRO = "intro"
 COLLECTING = "collecting"
 REFINING = "refining"
 REVIEWING = "reviewing"
 COMPLETE = "complete"
@dataclass
class SectionState:
 """Tracks progress within a single section."""
 key: str
 phase: Phase = Phase.INTRO
 answers: list[str] = field(default_factory=list)
 follow_up_index: int = 0
 refined_text: str = ""
 approved: bool = False
@dataclass
class ConversationState:
 """Tracks the overall conversation progress."""
 current_section_index: int = 0
 sections: dict[str, SectionState] = field(default_factory=dict)
 chat_history: list[dict] = field(default_factory=list)
 business_name: str = ""
 is_complete: bool = False
 def __post_init__(self):
 """Initialize section states for all 8 sections."""
 if not self.sections:
 for key in SECTION_ORDER:
 self.sections[key] = SectionState(key=key)
 @property
 def current_section_key(self) -> str:
 """Get the key of the current section."""
 if self.current_section_index < len(SECTION_ORDER):
 return SECTION_ORDER[self.current_section_index]
 return ""
 @property
 def current_section(self) -> SectionState:
 """Get the current section state."""
 return self.sections[self.current_section_key]
 @property
 def progress_fraction(self) -> float:
 """Return completion progress as a float from 0.0 to 1.0."""
 completed = sum(1 for s in self.sections.values() if s.approved)
 return completed / len(SECTION_ORDER)
def get_welcome_message() -> str:
 """Generate the initial welcome message."""
 return (
 "# Welcome to Grant-Ready! \n\n"
 "I'm here to help you create a **professional business plan** — "
 "the kind that grant reviewers and loan officers love to see.\n\n"
 "We'll work through **8 short sections** together. I'll ask you "
 "questions in plain language, and then I'll write each section for "
 "you in polished business plan style.\n\n"
 "**The whole thing takes about 20-30 minutes.** You can stop and "
 "come back anytime.\n\n"
 "---\n\n"
 "Before we dive in — **what's the name of your business?**"
 )
def process_message(state: ConversationState, user_message: str) -> str:
 """
 Process a user message and return the assistant's response.
 This is the main conversation engine. It determines what phase
 we're in and routes accordingly.
 Args:
 state: The current conversation state (mutated in place).
 user_message: The user's latest message.
 Returns:
 The assistant's response string.
 """
 # -- Step 0: Capture business name if we don't have it yet
 if not state.business_name:
 state.business_name = user_message.strip()
 state.chat_history.append({"role": "user", "content": user_message})
 # Start section 1
 section_def = SECTION_PROMPTS[state.current_section_key]
 intro = (
 f"**{state.business_name}** — love it! Let's build your plan.\n\n"
 f"---\n\n"
 f"## Section {section_def['number']} of 8: {section_def['name']}\n\n"
 f"{section_def['intro']}"
 )
 state.chat_history.append({"role": "assistant", "content": intro})
 return intro
 # -- Add user message to history
 state.chat_history.append({"role": "user", "content": user_message})
 section = state.current_section
 section_def = SECTION_PROMPTS[section.key]
 # -- Phase: INTRO or COLLECTING — gather answers
 if section.phase in (Phase.INTRO, Phase.COLLECTING):
 section.phase = Phase.COLLECTING
 section.answers.append(user_message)
 # Check if we have more follow-up questions
 if section.follow_up_index < len(section_def["follow_ups"]):
 follow_up = section_def["follow_ups"][section.follow_up_index]
 section.follow_up_index += 1
 # Use Llama to make the follow-up feel conversational
 bridge_messages = state.chat_history + [
 {
 "role": "user",
 "content": (
 f"[SYSTEM: The user just answered a question about "
 f"{section_def['name']}. Briefly acknowledge their answer "
 f"(1 sentence, be encouraging), then ask this next question: "
 f'"{follow_up}". Keep it warm and conversational.]'
 ),
 }
 ]
 response = engine.generate(SYSTEM_PROMPT, bridge_messages)
 state.chat_history.append({"role": "assistant", "content": response})
 return response
 else:
 # All follow-ups done — move to refining
 section.phase = Phase.REFINING
 return _refine_section(state, section, section_def)
 # -- Phase: REVIEWING — user is approving/editing the refined text
 elif section.phase == Phase.REVIEWING:
 lower = user_message.lower().strip()
 if any(word in lower for word in ["yes", "looks good", "approve", "perfect", "good",  # Approved — mark complete and move to next section
 section.approved = True
 section.phase = Phase.COMPLETE
 state.current_section_index += 1
 if state.current_section_index >= len(SECTION_ORDER):
 # All sections done!
 state.is_complete = True
 response = (
 "# Your Business Plan is Complete!\n\n"
 f"Congratulations! You just built a professional business "
 f"plan for **{state.business_name}**.\n\n"
 f"Click the **Download PDF** button below to get your "
 f"formatted business plan document.\n\n"
 f"You should be incredibly proud — most people never get "
 f"this far. Now go get that funding! "
 )
 else:
 # Start next section
 next_def = SECTION_PROMPTS[state.current_section_key]
 response = (
 f" Section {section_def['number']} — locked in!\n\n"
 f"---\n\n"
 f"## Section {next_def['number']} of 8: {next_def['name']}\n\n"
 f"{next_def['intro']}"
 )
 state.sections[state.current_section_key].phase = Phase.COLLECTING
 state.chat_history.append({"role": "assistant", "content": response})
 return response
 else:
 # User wants changes — send back to Llama for revision
 revision_messages = state.chat_history + [
 {
 "role": "user",
 "content": (
 f"[SYSTEM: The user wants to revise the {section_def['name']} "
 f"section. Their feedback: \"{user_message}\". "
 f"Here is the current draft:\n\n{section.refined_text}\n\n"
 f"Revise the section based on their feedback. Show them "
 f"the full updated version and ask if it looks good now.]"
 ),
 }
 ]
 response = engine.generate(SYSTEM_PROMPT, revision_messages)
 section.refined_text = response
 state.chat_history.append({"role": "assistant", "content": response})
 return response
 # -- Fallback: use Llama to handle unexpected input
 response = engine.generate(SYSTEM_PROMPT, state.chat_history)
 state.chat_history.append({"role": "assistant", "content": response})
 return response
def _refine_section(
 state: ConversationState,
 section: SectionState,
 section_def: dict,
) -> str:
 """Use Llama to refine the user's answers into professional prose."""
 answers_text = "\n".join(
 f"- {answer}" for answer in section.answers
 )
 refinement_prompt = section_def["refinement_prompt"].format(
 answers=answers_text
 )
 refinement_messages = [
 {
 "role": "user",
 "content": (
 f"Business name: {state.business_name}\n\n"
 f"{refinement_prompt}\n\n"
 f"After writing the section, add a line break and then ask: "
 f"'Does this look good, or would you like me to change anything?'"
 ),
 }
 ]
 response = engine.generate(SYSTEM_PROMPT, refinement_messages)
 section.refined_text = response
 section.phase = Phase.REVIEWING
 state.chat_history.append({"role": "assistant", "content": response})
 return response
