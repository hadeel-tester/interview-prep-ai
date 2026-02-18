import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Import from my modules
from prompts import PROMPT_TECHNIQUES
from utils import validate_inputs, is_valid_input
from chatbot import start_interview, send_message, end_interview

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "interview_config" not in st.session_state:
    st.session_state.interview_config = {}

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
# Auto-handle technique for Mock Interview
if prep_type == "Mock Interview":
    # Mock Interview ALWAYS uses Role-Based (best for interviewer persona)
    technique = "Role-Based"
    st.sidebar.info("🎭 **Mock Interview mode:** Using Role-Based technique (interviewer persona)")
else:
    # Regular modes - user can choose any technique
    technique = st.sidebar.selectbox(
        "🧪 Prompt Technique",
        options=list(PROMPT_TECHNIQUES.keys()),
        format_func=lambda x: PROMPT_TECHNIQUES[x]["label"]
    )
    st.sidebar.info(f"**How it works:** {PROMPT_TECHNIQUES[technique]['description']}")

    
# === OPENAI MODEL SETTINGS (COLLAPSIBLE) ===
with st.sidebar.expander("🤖 OpenAI Model Settings", expanded=False):
    # Model selector
    model = st.selectbox(
        "Model",
        options=[
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ],
        index=1,  # Default to gpt-4o-mini
        help="gpt-4o-mini is cost-effective and fast. gpt-4o is more capable but pricier."
    )

    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower = more focused, higher = more creative. Range: 0-2"
    )

    # Max Tokens
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help="Maximum length of the response. More tokens = longer responses but higher cost."
    )

    # Top P
    top_p = st.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Nucleus sampling. Lower = more deterministic. Use this OR temperature, not both at extremes."
    )

    # Frequency Penalty
    frequency_penalty = st.slider(
        "Frequency Penalty",
        min_value=0.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Reduces repetition. Higher values = less likely to repeat phrases. Range: 0-2"
    )

    # Presence Penalty
    presence_penalty = st.slider(
        "Presence Penalty",
        min_value=0.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Encourages new topics. Higher values = more likely to talk about new subjects. Range: 0-2"
    )

    st.caption("💡 **Tip:** Start with defaults, then experiment!")

# --- MAIN INPUT AREA ---
if prep_type == "Mock Interview":
    # === MOCK INTERVIEW MODE (CHATBOT) ===
    st.markdown("### 🎭 Interactive Mock Interview Mode")
    st.info("💡 This is a real-time conversation. The AI interviewer will ask questions and respond to your answers.")
    
    # Show interview controls
    if not st.session_state.interview_active:
        # Interview not started - show setup interface
        
        # Optional: Job description input
        job_description = st.text_area(
            "📄 Job Description (Optional but recommended)",
            placeholder="Paste the actual job description you're applying for. This will help the AI tailor interview questions to the specific role.",
            height=200,
            help="Providing the real JD makes the mock interview much more realistic and useful!"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Ready to begin your mock interview?**")
            st.caption(f"Role: {role if role else 'Not set'} | Difficulty: {difficulty}")
            if job_description.strip():
                st.caption(f"✅ Job description provided ({len(job_description)} characters)")
        with col2:
            if st.button("🎬 Start Interview", type="primary", disabled=not role):
                if not role:
                    st.warning("⚠️ Please enter a Job Role in the sidebar first!")
                else:
                    # Validate job role first
                    with st.spinner("🔍 Validating job role..."):
                        job_valid, job_reason, _, _ = validate_inputs(role, job_description if job_description.strip() else "")
                    
                    if not job_valid:
                        st.error(f"❌ **Invalid Job Role:** {job_reason}")
                        st.info("💡 Try something like: 'Software Engineer', 'Product Manager', 'Data Scientist'")
                    else:
                        # Start the interview with JD context
                        model_settings = {
                            "model": model,
                            "temperature": temperature,
                            "max_tokens": max_tokens,
                            "top_p": top_p,
                            "frequency_penalty": frequency_penalty,
                            "presence_penalty": presence_penalty,
                            "job_description": job_description  # ← Pass JD to interview
                        }
                        with st.spinner("🎬 Starting your interview..."):
                            start_interview(role, difficulty, technique, model_settings)
                        st.rerun()
    
    else:
        # Interview is active - show ONLY chat interface (no text area)
        st.markdown("---")
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="👔"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
        
        # Chat input
        user_input_chat = st.chat_input("Type your answer here...")
        
        if user_input_chat:
            with st.spinner("💭 Interviewer is thinking..."):
                send_message(user_input_chat)
            st.rerun()
        
        # End interview button
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col3:
            if st.button("🛑 End Interview", type="secondary"):
                end_interview()
                st.rerun()
        with col2:
            st.caption(f"💬 {len([m for m in st.session_state.messages if m['role'] == 'user'])} exchanges")

else:
    # === REGULAR MODE (all other prep types) ===
    user_input = st.text_area(
        "Your input (job description, topic, or just press Generate!)",
        placeholder="Paste a job description here, or describe what you want to practice...",
        height=150
    )
    
    if st.button("🚀 Generate Interview Prep", type="primary"):
        # Show current settings in an expander
        with st.expander("🔧 Active Settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Model", model)
                st.metric("Temperature", f"{temperature:.1f}")
                st.metric("Max Tokens", max_tokens)
            with col2:
                st.metric("Top P", f"{top_p:.2f}")
                st.metric("Frequency Penalty", f"{frequency_penalty:.1f}")
                st.metric("Presence Penalty", f"{presence_penalty:.1f}")

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
                            model=model,  # ← Use selected model from sidebar
                            messages=[
                                {"role": "system", "content": system},
                                {"role": "user", "content": user_prompt}
                            ],
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            frequency_penalty=frequency_penalty,
                            presence_penalty=presence_penalty
                        )
                        result = response.choices[0].message.content
                        
                        # Display results based on technique
                        if technique in ["JSON Basic", "JSON Detailed"]:
                            st.success(f"✅ Results using **{PROMPT_TECHNIQUES[technique]['label']}**:")
                            try:
                                import json
                                parsed = json.loads(result)
                                st.json(parsed)  # Renders JSON nicely in Streamlit

                                # Download button
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