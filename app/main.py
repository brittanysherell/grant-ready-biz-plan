"""
Grant-Ready Business Plan Writer — Main Streamlit Application
This is the entry point for the app. Run with:
 streamlit run app/main.py
"""
import streamlit as st
from app.config import config
from app.conversation import (
 ConversationState,
 get_welcome_message,
 process_message,
)
from app.plan_builder import build_plan
from app.pdf_export import generate_pdf
from app.prompts import SECTION_ORDER, SECTION_PROMPTS
# ======================================================================
# PAGE CONFIGURATION
# ======================================================================
st.set_page_config(
 page_title=config.APP_TITLE,
 page_icon=" ",
 layout="centered",
 initial_sidebar_state="expanded",
)
# ======================================================================
# CUSTOM STYLING
# ======================================================================
st.markdown(
 """
 <style>
 @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+ .stApp {
 font-family: 'DM Sans', sans-serif;
 }
 h1, h2, h3 {
 font-family: 'DM Serif Display', serif !important;
 }
 .main-header {
 text-align: center;
 padding: 1.5rem 0 1rem;
 }
 .main-header h1 {
 font-size: 2.2rem;
 margin-bottom: 0.3rem;
 }
 .main-header p {
 color: #777;
 font-size: 1rem;
 }
 .progress-label {
 font-size: 0.85rem;
 color: #888;
 margin-bottom: 0.3rem;
 }
 .section-badge {
 display: inline-block;
 background: #f0f4ff;
 color: #4a6cf7;
 padding: 0.2rem 0.7rem;
 border-radius: 999px;
 font-size: 0.8rem;
 font-weight: 600;
 margin-bottom: 0.5rem;
 }
 </style>
 """,
 unsafe_allow_html=True,
)
# ======================================================================
# SESSION STATE INITIALIZATION
# ======================================================================
if "conversation" not in st.session_state:
 st.session_state.conversation = ConversationState()
if "messages" not in st.session_state:
 st.session_state.messages = []
 # Add welcome message
 welcome = get_welcome_message()
 st.session_state.messages.append({"role": "assistant", "content": welcome})
state: ConversationState = st.session_state.conversation
# ======================================================================
# SIDEBAR — Progress Tracker
# ======================================================================
with st.sidebar:
 st.markdown("## Your Progress")
 st.progress(state.progress_fraction)
 completed = sum(1 for s in state.sections.values() if s.approved)
 st.caption(f"{completed} of {len(SECTION_ORDER)} sections complete")
 st.markdown("---")
 for key in SECTION_ORDER:
 section_def = SECTION_PROMPTS[key]
 section_state = state.sections[key]
 if section_state.approved:
 icon = " "
 elif key == state.current_section_key and state.business_name:
 icon = " "
 else:
 icon = " "
 st.markdown(
 f"{icon} **{section_def['number']}.** {section_def['name']}"
 )
 st.markdown("---")
 st.caption(
 f"Powered by Llama via {config.LLM_PROVIDER.title()}\n\n"
 f"Built by MDOT Global"
 )
 # Reset button
 if st.button(" Start Over", use_container_width=True):
 st.session_state.conversation = ConversationState()
 st.session_state.messages = []
 welcome = get_welcome_message()
 st.session_state.messages.append(
 {"role": "assistant", "content": welcome}
 )
 st.rerun()
# ======================================================================
# MAIN HEADER
# ======================================================================
st.markdown(
 f"""
 <div class="main-header">
 <h1> {config.APP_TITLE}</h1>
 <p>{config.APP_SUBTITLE}</p>
 </div>
 """,
 unsafe_allow_html=True,
)
# ======================================================================
# CHAT INTERFACE
# ======================================================================
# Display all messages
for message in st.session_state.messages:
 with st.chat_message(message["role"]):
 st.markdown(message["content"])
# Chat input
if user_input := st.chat_input(
 "Type your answer here...",
 disabled=state.is_complete,
):
 # Display user message
 with st.chat_message("user"):
 st.markdown(user_input)
 st.session_state.messages.append({"role": "user", "content": user_input})
 # Process and display response
 with st.chat_message("assistant"):
 with st.spinner("Thinking..."):
 response = process_message(state, user_input)
 st.markdown(response)
 st.session_state.messages.append(
 {"role": "assistant", "content": response}
 )
 st.rerun()
# ======================================================================
# PDF DOWNLOAD — Show when plan is complete
# ======================================================================
if state.is_complete:
 st.markdown("---")
 st.markdown("### Download Your Business Plan")
 plan = build_plan(state)
 col1, col2 = st.columns(2)
 with col1:
 pdf_bytes = generate_pdf(plan)
 st.download_button(
 label=" Download PDF",
 data=pdf_bytes,
 file_name=f"{state.business_name.replace(' ', '_')}_Business_Plan.pdf",
 mime="application/pdf",
 use_container_width=True,
 )
 with col2:
 md_text = plan.to_markdown()
 st.download_button(
 label=" Download Markdown",
 data=md_text,
 file_name=f"{state.business_name.replace(' ', '_')}_Business_Plan.md",
 mime="text/markdown",
 use_container_width=True,
 )


