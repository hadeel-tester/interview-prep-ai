import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#api_key = os.environ.get("OPENAI_API_KEY")
#if not api_key:
#    raise EnvironmentError("Set OPENAI_API_KEY environment variable.")
#client = OpenAI(api_key=api_key)

# --- PAGE SETUP ---
st.set_page_config(page_title="Interview Prep AI", page_icon="🎯")
st.title("🎯 AI Interview Preparation Assistant")
st.markdown("Practice and prepare for your dream job interview!")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Settings")

role = st.sidebar.text_input("Job Role", placeholder="e.g. Software Engineer")
difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
prep_type = st.sidebar.selectbox("What do you want to practice?", [
    "Technical Questions",
    "Behavioral Questions (STAR method)",
    "Questions to ask the Interviewer",
    "Analyze a Job Description",
    "Mock Interview"
])
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)

# --- SECURITY GUARD: block empty or irrelevant inputs ---
def is_valid_input(text):
    blocked_words = ["ignore", "jailbreak", "forget your instructions", "pretend you are"]
    if not text or len(text.strip()) < 5:
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
        temperature=0,  # deterministic for validation
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

# --- SYSTEM PROMPTS (5 techniques) ---
system_prompts = {
    "Technical Questions": """You are an expert technical interviewer with 15 years of experience at top tech companies.
    Generate {difficulty} difficulty technical interview questions for a {role} position.
    For each question: provide the question, what the interviewer is testing, and a model answer.
    Use Chain-of-Thought: think step by step about what skills are needed for this role.""",

    "Behavioral Questions (STAR method)": """You are a senior HR professional and career coach.
    Generate behavioral interview questions using the STAR method (Situation, Task, Action, Result).
    Example format:
    Q: "Tell me about a time you handled conflict."
    STAR Guide: Situation - describe workplace conflict | Task - your responsibility | Action - steps you took | Result - outcome achieved.
    Now generate {difficulty} questions for a {role} role.""",

    "Questions to ask the Interviewer": """You are a career coach helping candidates impress interviewers.
    Generate smart, thoughtful questions a candidate should ask at the end of an interview for a {role} role.
    Zero-shot: Generate questions across these categories: culture, growth, team, role expectations, success metrics.""",

    "Analyze a Job Description": """You are an interview strategy expert.
    Analyze the provided job description and extract:
    1. Key technical skills to prepare for
    2. Likely interview topics
    3. Red flags or challenges
    4. Suggested preparation strategy
    Think step by step before giving your final answer.""",

    "Mock Interview": """You are roleplaying as a {difficulty}-style interviewer for a {role} position.
    - Easy: friendly and encouraging
    - Medium: professional and neutral  
    - Hard: strict and challenging
    Ask one question at a time. Wait for the candidate's answer, then give brief feedback and move to the next question.
    Start by introducing yourself and asking the first question."""
}

# --- MAIN INPUT AREA ---
user_input = st.text_area(
    "Your input (job description, topic, or just press Generate!)",
    placeholder="Paste a job description here, or describe what you want to practice...",
    height=150
)

if st.button("🚀 Generate Interview Prep", type="primary"):
    if not role:
        st.warning("⚠️ Please enter a Job Role in the sidebar first!")
    else:
        # --- RUN GUARDRAIL VALIDATION FIRST ---
        with st.spinner("🔍 Validating your inputs..."):
            job_valid, job_reason, input_valid, input_reason = validate_inputs(role, user_input)
        
        # Show errors if validation fails
        has_error = False
        
        if not job_valid:
            st.error(f"❌ **Invalid Job Role:** {job_reason}")
            st.info("💡 Try something like: 'Software Engineer', 'Product Manager', 'Data Scientist', 'Nurse'")
            has_error = True
            
        if not input_valid:
            st.error(f"❌ **Invalid Input:** {input_reason}")
            st.info("💡 Please enter a real job description or leave the field empty.")
            has_error = True
        
        # Only proceed if everything is valid
        if not has_error:
            system = system_prompts[prep_type].format(role=role, difficulty=difficulty)
            user_prompt = f"Help me prepare for a {role} interview. Focus: {prep_type}. Difficulty: {difficulty}."
            if user_input.strip():
                user_prompt += f"\n\nAdditional context:\n{user_input}"

            with st.spinner("✨ Preparing your interview materials..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=temperature,
                        max_tokens=1000
                    )
                    result = response.choices[0].message.content
                    st.success("✅ Here's your interview preparation:")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")