import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPT_TECHNIQUES
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
# Prompt technique selector
technique = st.sidebar.selectbox(
    "🧪 Prompt Technique",
    options=list(PROMPT_TECHNIQUES.keys()),
    format_func=lambda x: PROMPT_TECHNIQUES[x]["label"]
)
st.sidebar.info(f"**How it works:** {PROMPT_TECHNIQUES[technique]['description']}")
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
    """Use OpenAI to check if job role is real."""
    
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



# TODO: Mock interview with interactive back-and-forth is complex to implement in a single response. Consider breaking it down into multiple steps or using a different approach for this technique.

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
        # Get system prompt from selected technique
            system = PROMPT_TECHNIQUES[technique]["system_prompt"]
            user_prompt = f"Job Role: {role}\nPreparation Type: {prep_type}\nDifficulty: {difficulty}"
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
                    
                    st.success(f"✅ Results using **{PROMPT_TECHNIQUES[technique]['label']}** technique:")
                    
                    # Handle JSON output differently
                    if technique == "JSON Basic" or technique == "JSON Detailed":
                        try:
                            import json
                            parsed = json.loads(result)
                            st.json(parsed)  # Renders JSON nicely in Streamlit

                            # Optional: Add download button
                            st.download_button(
                            label="📥 Download JSON",
                            data=json.dumps(parsed, indent=2),
                            file_name=f"interview_prep_{role.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                        except json.JSONDecodeError:
                            st.warning("⚠️ Response wasn't valid JSON. Displaying as text:")
                            st.code(result, language="json")
                    else:
                        st.success(f"✅ Results using **{PROMPT_TECHNIQUES[technique]['label']}** technique:")
                        st.markdown(result)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")