import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPT_TECHNIQUES
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def start_interview(role, difficulty, technique, model_settings):
    """Initialize a new mock interview session."""
    st.session_state.interview_active = True
    st.session_state.messages = []
    # Extract job description if provided
    job_description = model_settings.pop("job_description", "")
    
    st.session_state.interview_config = {
        "role": role,
        "difficulty": difficulty,
        "technique": technique,
        "model": model_settings["model"],
        "temperature": model_settings["temperature"],
        "max_tokens": model_settings["max_tokens"],
        "top_p": model_settings["top_p"],
        "frequency_penalty": model_settings["frequency_penalty"],
        "presence_penalty": model_settings["presence_penalty"]
    }
    
    # Get system prompt based on technique
    system_prompt = PROMPT_TECHNIQUES[technique]["system_prompt"]
    
    # Create initial interviewer message
    initial_prompt = f"""You are conducting a mock interview for a {role} position at {difficulty} difficulty level.
    if job_description.strip():
    initial_prompt += f"JOB DESCRIPTION:\n{job_description}\n\n"

   initial_prompt += Start by:
1. Briefly introducing yourself as the interviewer
2. Asking your first interview question

Keep it conversational and professional."""
    
    # Get interviewer's opening
    response = client.chat.completions.create(
        model=model_settings["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": initial_prompt}
        ],
        temperature=model_settings["temperature"],
        max_tokens=model_settings["max_tokens"],
        top_p=model_settings["top_p"],
        frequency_penalty=model_settings["frequency_penalty"],
        presence_penalty=model_settings["presence_penalty"]
    )
    
    opening = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": opening})


def send_message(user_message):
    """Send a message in the interview and get response."""
    config = st.session_state.interview_config
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Build conversation for API (include system prompt + all messages)
    system_prompt = PROMPT_TECHNIQUES[config["technique"]]["system_prompt"]
    
    api_messages = [{"role": "system", "content": system_prompt}]
    api_messages.extend(st.session_state.messages)
    
    # Get interviewer response
    response = client.chat.completions.create(
        model=config["model"],
        messages=api_messages,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        frequency_penalty=config["frequency_penalty"],
        presence_penalty=config["presence_penalty"]
    )
    
    assistant_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})


def end_interview():
    """End the mock interview session."""
    st.session_state.interview_active = False
    st.session_state.messages = []
    st.session_state.interview_config = {}