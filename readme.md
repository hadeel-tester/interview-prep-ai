# AI Interview Preparation Assistant

The **AI Interview Preparation Assistant** is a Streamlit-based web application designed to help users practice for technical and behavioral interviews. It generates high‑quality interview questions using OpenAI models and allows users to customize difficulty, topic, and creativity settings.  
This project is built as part of the Turing College AI Engineering curriculum.

---

## 🚀 Features

- Generate interview questions for any topic or job role  
- Adjustable difficulty levels (Easy, Medium, Hard)  
- Temperature control for creativity  
- Five different system prompts using various prompt‑engineering techniques  
- Input validation and basic guardrails  
- Clean, simple single‑page UI built with Streamlit  
- Modular code structure for easy maintenance and extension  

---

## 📁 Folder Structure

```text
interview_practice_app/
│
├── app.py                     # Main Streamlit application
│
├── prompts/                   # Required 5 system prompts
│   ├── base_prompt.txt
│   ├── few_shot_prompt.txt
│   ├── role_prompt.txt
│   ├── cot_prompt.txt
│   └── style_prompt.txt
│
├── utils/
│   ├── openai_client.py       # Handles OpenAI API calls
│   ├── guardrails.py          # Input validation & safety checks
│   └── helpers.py             # Formatting and shared utilities
│
├── assets/
│   └── logo.png               # Optional branding assets
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .env                       # environment variables
