from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_valid_input(text):
    """Basic input validation - checks for blocked keywords/prompt injection."""
    blocked_words = ["ignore", "jailbreak", "forget your instructions", "pretend you are",
                     "system prompt", "bypass", "override", "no rules", "no guidelines"
                      "remove restrictions"]
    if not text or len(text.strip()) < 5:
        return False
    if len(text) > 10000:  # Prevent extremely long inputs (API abuse)
        return False
    for word in blocked_words:
        if word.lower() in text.lower():
            return False
    return True


def validate_inputs(role, user_input):
    """Use OpenAI to check if job role is real and input is not gibberish."""
    
    validation_prompt = f"""You are an input validator. Analyze the following inputs and respond ONLY in this exact format, nothing else:

JOB_VALID: true/false
JOB_REASON: one sentence explanation
INPUT_VALID: true/false  
INPUT_REASON: one sentence explanation

Inputs to validate:
- Job Role: "{role}"
- User Input: "{user_input if user_input.strip() else 'empty'}"

Rules:
- JOB_VALID is true only if it's a real, recognized job title that exists in the real world (e.g. "Software Engineer", "Nurse", "Teacher"). Mark false for gibberish like "asdfgh", fake jobs like "Dragon Trainer", or nonsense like "abc123".
- INPUT_VALID is true if the user input is either: empty (that's fine), a real sentence/paragraph, or a job description. Mark false only if it's clear gibberish like "aaaaaa", "xyz123", random keyboard smashing, or completely unrelated nonsense."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": validation_prompt}],
        temperature=0,
        max_tokens=100
    )
    
    result = response.choices[0].message.content.strip()
    
    # Parse the response
    lines = result.split('\n')
    parsed = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            parsed[key.strip()] = value.strip()
    
    job_valid = parsed.get('JOB_VALID', 'false').lower() == 'true'
    job_reason = parsed.get('JOB_REASON', 'Invalid job role.')
    input_valid = parsed.get('INPUT_VALID', 'false').lower() == 'true'
    input_reason = parsed.get('INPUT_REASON', 'Invalid input.')
    
    return job_valid, job_reason, input_valid, input_reason