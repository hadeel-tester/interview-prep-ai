# 🎯 AI Interview Preparation Assistant

A smart, AI-powered interview preparation tool built with Streamlit and OpenAI's GPT models. Practice technical questions, behavioral interviews, and even participate in interactive mock interviews with an AI interviewer.

**Built as part of the Turing College AI Engineering curriculum.**

🔗 **[Live Demo](https://app-url.streamlit.app)** _(Add this after deployment)_

---

## ✨ Features

### Core Functionality
- 🎓 **Multiple Prep Modes**: Technical questions, behavioral (STAR method), job description analysis, questions to ask interviewers
- 🎭 **Interactive Mock Interviews**: Real-time conversational practice with AI interviewer (chatbot mode)
- 📊 **Structured JSON Outputs**: Export interview prep data in two JSON formats (basic & detailed)
- 🎚️ **Advanced Model Controls**: Fine-tune temperature, top-p, frequency penalty, presence penalty, and max tokens

### Prompt Engineering Techniques
Implements 6 different prompting strategies:
- **Zero-Shot**: Direct instruction without examples
- **Few-Shot**: Learning from provided examples
- **Role-Based**: AI persona as experienced recruiter
- **Chain-of-Thought**: Step-by-step reasoning
- **JSON Basic**: Simple structured output
- **JSON Detailed**: Comprehensive nested output

### Security & Validation
- 🔐 Environment variable protection for API keys
- 🛡️ Prompt injection blocking (9+ attack patterns)
- 🤖 AI-powered input validation (detects gibberish and fake job roles)
- ✅ Multi-layer defense against misuse

---

## 🏗️ Architecture
```
interview-prep-app/
│
├── app.py                 # Main Streamlit UI and routing logic
├── chatbot.py             # Mock interview conversation engine
├── utils.py               # Input validation and security guardrails
├── prompts.py             # System prompt templates (6 techniques)
│
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .env                   # API keys (not committed)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/hadeel-tester/ai-interview-prep-assistant.git
   cd ai-interview-prep-assistant
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Set up your API key**
```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-actual-key-here
```

4. **Run the app**
```bash
   streamlit run app.py
```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

---

## 📖 Usage Guide

### Basic Interview Prep
1. Enter your **Job Role** in the sidebar (e.g., "Software Engineer")
2. Select **Difficulty Level**: Easy, Medium, or Hard
3. Choose **Prep Type**: Technical, Behavioral, Job Description Analysis, etc.
4. Select a **Prompt Technique** to see different AI approaches
5. (Optional) Paste a job description for tailored questions
6. Click **Generate Interview Prep**

### Mock Interview (Chatbot Mode)
1. Select **"Mock Interview"** from the prep type dropdown
2. Enter your job role
3. (Optional) Paste the actual job description you're applying for
4. Click **Start Interview**
5. Respond to the interviewer's questions in real-time
6. Get feedback and follow-up questions
7. Click **End Interview** when done

### Advanced Settings
- Expand **OpenAI Model Settings** to tune:
  - Model selection (GPT-4o, GPT-4o-mini, etc.)
  - Temperature (creativity level)
  - Max tokens (response length)
  - Frequency & presence penalties (control repetition)

---

## 🎓 Project Requirements Met

This project fulfills the following Turing College sprint requirements:

### Core Requirements ✅
- [x] 5+ system prompts with different techniques
- [x] Tuned OpenAI settings (temperature, top-p, frequency penalty, etc.)
- [x] Input validation and security guards
- [x] Single-page Streamlit interface

### Optional Tasks Completed ✅
**Medium Difficulty:**
- [x] All OpenAI settings exposed as user controls
- [x] Two structured JSON output formats
- [x] Deployed to the internet (Streamlit Cloud)

**Hard Difficulty:**
- [x] Full-fledged chatbot for mock interviews (session state + conversation history)

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o-mini / GPT-4o
- **Language**: Python 3.8+
- **Libraries**: 
  - `openai` - API client
  - `python-dotenv` - Environment variable management
  - `streamlit` - Web interface

---

## 🔒 Security

- API keys stored in `.env` file (never committed to Git)
- Prompt injection protection with keyword blocking
- AI-powered validation to prevent gibberish inputs
- Input length limits to prevent API abuse

---

## 🚢 Deployment

### Streamlit Cloud (Current)
This app is deployed on Streamlit Cloud. To deploy your own:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your `OPENAI_API_KEY` in the Secrets section:
```toml
   OPENAI_API_KEY = "sk-your-key-here"
```
5. Deploy!

### AWS (Planned)
Designed for scalable deployment on AWS EC2 with Docker containerization.

---

## 📊 Screenshots

_Add screenshots here after deployment:_
- Main interface
- Mock interview in action
- JSON output example
- Settings panel

---

## 🤝 Contributing

This is a learning project, but suggestions are welcome! Feel free to:
- Open an issue for bugs or feature requests
- Fork and submit pull requests
- Share feedback on the prompting techniques

---

## 📝 License

This project is created for educational purposes as part of the Turing College AI Engineering course.

---

## 👤 Author

- GitHub: [@hadeel-tester](https://github.com/hadeel-tester)
- LinkedIn: [Hadeel Ahmed](https://linkedin.com/in/hadeel-ahmed-software-tester/)
- Portfolio: [my-portfolio.com](https://my-portfolio.com)

---

## 🙏 Acknowledgments

- [Turing College](https://www.turingcollege.com/) for the curriculum and guidance
- OpenAI for the GPT API
- Streamlit for the amazing web framework

---

## 📞 Support

If you have questions about this project, please:
1. Check the [Issues](https://github.com/your-username/ai-interview-prep-assistant/issues) page
2. Review the code comments in each module
3. Reach out via LinkedIn

