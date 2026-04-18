# Grant-Ready Business Plan Writer

An open-source, AI-powered conversational tool that helps micro-business owners create a complete, grant-ready business plan — step by step.

Built using Meta’s Llama and designed for the Llama Impact Grants program.

**Created by MDOT Global**  
Brittany (Chief Strategy Officer)  
Marcus Glenn (CEO)

---

## 🚀 Overview

Millions of micro-business owners — including hair stylists, food truck operators, cleaning services, and freelancers — need a business plan to apply for grants, secure funding, or organize their operations. However, traditional solutions are often inaccessible.

**Common challenges include:**
- High cost of professional consultants ($2,000–$10,000)
- Overwhelming templates filled with complex jargon
- Lack of familiarity with business planning among first-generation entrepreneurs

**Grant-Ready Business Plan Writer** solves this by guiding users through a simple, conversational experience powered by AI. Users answer plain-language questions, and the system transforms their responses into a polished, professional business plan.

---

## ✨ Key Features

- **Conversational Workflow**  
  Guides users through 8 structured sections using natural dialogue

- **Plain Language Prompts**  
  No MBA jargon — designed for real-world users

- **Smart Follow-ups**  
  Llama asks clarifying questions when responses are incomplete or unclear

- **PDF Export**  
  Generates a clean, professional, downloadable business plan

- **Flexible Progress**  
  Complete sections individually and return anytime

- **Custom Knowledge Base**  
  Easily extend with industry-specific insights

- **Fully Open Source**  
  MIT licensed and free to use forever

---

## 🏗️ Architecture

```
grant-ready-biz-plan/
├── app/
│   ├── main.py              # Streamlit application entry point
│   ├── llm_engine.py       # Llama integration via Ollama or API
│   ├── conversation.py     # Conversation state machine
│   ├── plan_builder.py     # Builds business plan from responses
│   ├── pdf_export.py       # PDF generation module
│   ├── prompts.py          # System and section prompts
│   └── config.py           # App configuration
│
├── knowledge_base/
│   ├── sections.json       # Business plan structure
│   ├── examples.json       # Sample responses
│   └── industry_tips.json  # Industry-specific guidance
│
├── tests/
│   ├── test_conversation.py
│   ├── test_plan_builder.py
│   └── test_prompts.py
│
├── .github/
│   └── workflows/
│       └── ci.yml          # CI pipeline
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── LICENSE
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- One of the following:
  - Ollama (for local Llama inference)
  - Llama API key (Together AI, Fireworks, Replicate)

---

### 1. Clone the Repository

```bash
git clone https://github.com/brittanysherell/grant-ready-biz-plan.git
cd grant-ready-biz-plan
```

---

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Set Up Llama

#### Option A: Local (Recommended for Development)

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1:8b
```

#### Option B: Cloud API

```bash
cp .env.example .env
# Add your API key inside the .env file
```

---

### 4. Run the Application

```bash
streamlit run app/main.py
```

Then open your browser and go to:

```
http://localhost:8501
```

---

## 🧠 How It Works

The application guides users through 8 essential sections of a professional business plan:

| # | Section | Description |
|---|--------|------------|
| 1 | Executive Summary | Overview of the business |
| 2 | Business Description | What you do and who you serve |
| 3 | Market Analysis | Customers and competitors |
| 4 | Organization | Team structure |
| 5 | Products & Services | What you offer |
| 6 | Marketing Plan | How you attract customers |
| 7 | Financial Projections | Costs, pricing, revenue |
| 8 | Funding Request | Required funding and usage |

After each section:
- The AI refines user input into professional language
- The result is shown for user approval
- Users can edit before moving forward

---

## 🤝 Contributing

We welcome contributions from the community.

**Ways to contribute:**
- Add industry-specific tips in `knowledge_base/industry_tips.json`
- Translate prompts for multilingual support
- Improve PDF formatting
- Add export formats (DOCX, Google Docs)
- Write or improve tests

Please refer to `CONTRIBUTING.md` for detailed guidelines.

---

## 📜 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Meta AI for open-sourcing Llama
- Built for the **Llama Impact Grants Program**
- Developed by **MDOT Global** to empower underserved entrepreneurs

---

## 💡 Mission

Our goal is to democratize access to business planning tools by making them simple, affordable, and accessible to everyone — regardless of background or experience.

