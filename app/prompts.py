"""
Prompt templates for the Grant-Ready Business Plan Writer.
These prompts guide Llama through each section of the business plan,
using plain language that's accessible to first-time entrepreneurs.
"""
# ---------------------------------------------------------------------------
# SYSTEM PROMPT — Sets the overall persona and behavior
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are Grant-Ready, a warm and encouraging AI business plan \
coach. You help micro-business owners create professional business plans through \
friendly conversation.
YOUR PERSONALITY:
- Warm, encouraging, and patient — like a supportive mentor
- You use plain language, never MBA jargon
- You celebrate what the user already knows about their business
- You ask ONE question at a time and wait for the answer
- You gently ask follow-up questions when answers are too vague
YOUR RULES:
1. Never overwhelm the user. One question at a time.
2. If the user seems unsure, give a brief example to help them.
3. After collecting enough info for a section, summarize what you heard \
 back to the user in professional business plan language.
4. Ask the user to approve or edit your summary before moving on.
5. Keep summaries to 2-4 paragraphs per section. Concise and grant-ready.
6. If the user's answer is short, ask a follow-up to draw out more detail.
7. Always end your response with a clear next question or action.
NEVER:
- Use words like "synergy," "leverage," "paradigm," or "scalable ecosystem"
- Write more than 4 paragraphs at once
- Skip ahead without the user's confirmation
- Make up financial numbers the user didn't provide
"""
# ---------------------------------------------------------------------------
# SECTION DEFINITIONS — Each section has an intro, questions, and refinement
# ---------------------------------------------------------------------------
SECTION_PROMPTS = {
 "executive_summary": {
 "name": "Executive Summary",
 "number": 1,
 "intro": (
 "Let's start with the big picture! I'm going to ask you a few "
 "questions about your business, and then I'll help you write a "
 "polished Executive Summary — that's the first thing a grant "
 "reviewer reads.\n\n"
 "**First question:** Tell me about your business in your own words. "
 "What do you do, and why did you start it?"
 ),
 "follow_ups": [
 "Where is your business located, and how long have you been operating?",
 "What makes your business different from others that do something similar?",
 "What's your biggest goal for the next 1-2 years?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a professional Executive "
 "Summary for a business plan. Use 2-3 paragraphs. Write in third "
 "person (e.g., '[Business Name] is a...'). Keep it clear, confident, "
 "and free of jargon. This should read like it belongs in a grant "
 "application.\n\nUser's answers:\n{answers}"
 ),
 },
 "business_description": {
 "name": "Business Description",
 "number": 2,
 "intro": (
 "Great work on the Executive Summary! Now let's dig deeper into "
 "what your business actually does.\n\n"
 "**Question:** What product or service do you sell? Walk me through "
 "what a customer experiences from start to finish."
 ),
 "follow_ups": [
 "What problem does your business solve for your customers?",
 "Is your business registered as an LLC, sole proprietorship, corporation, or some "Do you operate from a physical location, online, or both?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Business Description "
 "section for a business plan. Cover: what the business does, "
 "the legal structure, location/operations model, and the core "
 "problem it solves. Use 2-3 paragraphs in third person. "
 "Professional but accessible tone.\n\nUser's answers:\n{answers}"
 ),
 },
 "market_analysis": {
 "name": "Market Analysis",
 "number": 3,
 "intro": (
 "Now let's talk about your market — the people who buy from you "
 "and the other businesses that do what you do.\n\n"
 "**Question:** Describe your ideal customer. Who are they? "
 "(Age, location, income level, what they care about)"
 ),
 "follow_ups": [
 "How many potential customers like this are in your area or target market?",
 "Who are your top 2-3 competitors? What do they charge?",
 "What do you do better than your competitors — why would someone choose you?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Market Analysis "
 "section for a business plan. Include: target customer profile, "
 "market size (use the user's estimates), competitive landscape, "
 "and competitive advantages. Use 2-3 paragraphs in third person. "
 "If the user gave rough numbers, present them professionally.\n\n"
 "User's answers:\n{answers}"
 ),
 },
 "organization": {
 "name": "Organization & Management",
 "number": 4,
 "intro": (
 "Let's talk about the people behind the business.\n\n"
 "**Question:** Is it just you running things, or do you have a "
 "team? Tell me about who does what."
 ),
 "follow_ups": [
 "What's your background or experience that makes you the right person to run this "Do you have any advisors, mentors, or partners who support you?",
 "Are you planning to hire anyone in the next year?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write an Organization & "
 "Management section for a business plan. Highlight the owner's "
 "qualifications, current team structure, and growth plans. "
 "Use 2-3 paragraphs in third person. Make the owner sound "
 "credible and capable.\n\nUser's answers:\n{answers}"
 ),
 },
 "products_services": {
 "name": "Products & Services",
 "number": 5,
 "intro": (
 "Let's get specific about what you offer.\n\n"
 "**Question:** List out your main products or services. "
 "For each one, what do you charge?"
 ),
 "follow_ups": [
 "What does it cost YOU to deliver each product or service? (materials, time, supp "Are there any products or services you want to add in the future?",
 "Do you have any special certifications, patents, or proprietary processes?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Products & Services "
 "section for a business plan. Detail the offerings, pricing, "
 "costs, margins (if calculable), future offerings, and any "
 "intellectual property. Use 2-3 paragraphs in third person.\n\n"
 "User's answers:\n{answers}"
 ),
 },
 "marketing_plan": {
 "name": "Marketing & Sales Strategy",
 "number": 6,
 "intro": (
 "Now let's talk about how you get customers!\n\n"
 "**Question:** How do people currently find out about your "
 "business? (Social media, word of mouth, ads, events, etc.)"
 ),
 "follow_ups": [
 "What's working best for you right now in terms of getting new customers?",
 "How much do you spend on marketing each month (even if it's $0)?",
 "If you had more resources, what marketing would you want to do?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Marketing & Sales "
 "Strategy section for a business plan. Cover: current channels, "
 "what's working, budget, and growth strategy. Use 2-3 paragraphs "
 "in third person. Frame even modest efforts professionally.\n\n"
 "User's answers:\n{answers}"
 ),
 },
 "financial_projections": {
 "name": "Financial Projections",
 "number": 7,
 "intro": (
 "I know finances can feel intimidating, but we'll keep this "
 "simple. I just need some basic numbers.\n\n"
 "**Question:** How much money does your business bring in per "
 "month right now? (It's okay if it's $0 — just be honest!)"
 ),
 "follow_ups": [
 "What are your monthly expenses? (rent, supplies, software, insurance, etc.)",
 "What do you expect your monthly revenue to be in 12 months?",
 "What about in 3 years — where do you see the numbers going?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Financial Projections "
 "section for a business plan. Present current revenue, expenses, "
 "and projected growth. Use the EXACT numbers the user provided — "
 "do not invent figures. If the user gave ranges, use the midpoint. "
 "Use 2-3 paragraphs in third person. Include a simple revenue "
 "vs. expenses comparison.\n\nUser's answers:\n{answers}"
 ),
 },
 "funding_request": {
 "name": "Funding Request",
 "number": 8,
 "intro": (
 "Last section — you're almost done! \n\n"
 "**Question:** How much funding are you looking for, and what "
 "would you use it for? (Be as specific as you can — equipment, "
 "inventory, marketing, hiring, etc.)"
 ),
 "follow_ups": [
 "Over what time period would you spend this money? (e.g., 6 months, 1 year)",
 "What impact will this funding have on your business? (more customers, new locati "Have you received any funding or loans before?",
 ],
 "refinement_prompt": (
 "Based on the user's answers below, write a Funding Request "
 "section for a business plan. State the amount requested, "
 "specific use of funds, timeline, expected impact, and any "
 "previous funding history. Use 2-3 paragraphs in third person. "
 "Make a compelling case for why this investment will pay off.\n\n"
 "User's answers:\n{answers}"
 ),
 },
}
# ---------------------------------------------------------------------------
# HELPER: Get ordered list of section keys
# ---------------------------------------------------------------------------
SECTION_ORDER = [
 "executive_summary",
 "business_description",
 "market_analysis",
 "organization",
 "products_services",
 "marketing_plan",
 "financial_projections",
 "funding_request",
]
def get_section_by_number(number: int) -> dict | None:
 """Get a section definition by its 1-based number."""
 for key in SECTION_ORDER:
 if SECTION_PROMPTS[key]["number"] == number:
 return SECTION_PROMPTS[key]
 return None
def get_section_key_by_number(number: int) -> str | None:
 """Get a section key by its 1-based number."""
 for key in SECTION_ORDER:
 if SECTION_PROMPTS[key]["number"] == number:
 return key
 return None
