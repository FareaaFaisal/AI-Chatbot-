# 🤖 Fareaa's AI Chatbot

A beautiful, animated chatbot built using **Streamlit** and **Gemini API**, designed to deliver real-time, intelligent conversational responses in a clean neon-themed UI.

---

## 🚀 Features

- 💬 Interactive AI Chat with Gemini API
- 🎨 Custom dark-themed UI with animated neon background
- 📥 User-friendly chat input form
- 🔒 Secrets handled securely with `.env` file
- ⚡ Fast response using async request handling
- 🌐 Deployable via Streamlit or local server

---

🛠️ Tech Stack
Streamlit — Web UI Framework for building interactive apps

Chainlit — Agentic AI Framework for building and debugging LLM-powered apps

Gemini API — Conversational AI by Google

Python 3.10+ — Programming language used

.env — For secure API key management (recommended to store secrets locally and use st.secrets on Streamlit Cloud)

---

## 🔐 Environment Setup

Create a `.env` file in the root directory with:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
📦 Installation & Usage
bash
# Clone the repo
git clone https://github.com/FareaaFaisal/AI-Chatbot-.git
cd AI-Chatbot-

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the chatbot
streamlit run app.py
❗ Important Notes
The .env file is listed in .gitignore, but if it was accidentally committed before, use git rm --cached .env to stop tracking it.

Do not share your API keys publicly.

👩‍💻 Author
Fareaa Faisal
GitHub: @FareaaFaisal

📜 License
This project is open-source and free to use under the MIT License.

