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

interview_practice_app/
│
├── app.py                     # 📱 Main Streamlit app (UI, layout, logic)
│
├── prompts/                   # 💬 Prompt templates for different techniques
│   ├── base_prompt.txt        # 🧱 Base system prompt
│   ├── few_shot_prompt.txt    # 🎯 Few-shot examples
│   ├── role_prompt.txt        # 🎭 Role-based interviewer persona
│   ├── cot_prompt.txt         # 🧠 Chain-of-thought prompt
│   └── style_prompt.txt       # 🎨 Style / tone prompt
│
├── utils/                     # 🛡️ Validation + helper functions
│   └── input_validation.py    # 🔍 Security guardrails
│
├── requirements.txt           # 📦 Python dependencies
├── README.md                  # 📘 Project documentation
└── .env                       # 🔑 API key (NOT COMMITED)

