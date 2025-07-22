import os
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Model setup
external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(model=model, model_provider=external_client)

agent = Agent(
    name="GeminiBot",
    instructions="You're a helpful assistant.",
    model=model,
)

st.set_page_config(page_title="Neon Chatbot", layout="wide")

# ===== CSS =====
st.markdown("""
<style>
html, body, .stApp {
    overflow: hidden !important;
    height: 100vh;
}
::-webkit-scrollbar {
    display: none;
}
#bg-animation {
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background-image:
        radial-gradient(circle, #00f0ff44 1%, transparent 30%),
        radial-gradient(circle, #ff00ff44 1%, transparent 30%),
        radial-gradient(circle, #00ff8844 1%, transparent 30%);
    background-size: 20% 20%;
    animation: spin 25s linear infinite;
    z-index: 0;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.stApp {
    background-color: transparent !important;
    z-index: 2;
    height: 100vh;
    overflow: hidden;
    position: relative;
}
#chat-wrapper {
    position: absolute;
    top: 70px;
    bottom: 0px;
    left: 0;
    right: 0;
    overflow-y: auto;
    padding: 20px;
    box-sizing: border-box;
}
.chat-box {
    background: rgba(0,0,0,0.6);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 10px;
    color: white;
}
.user {
    background-color: #00f0ff33;
    text-align: right;
}
.bot {
    background-color: #ffffff11;
    text-align: left;
}

textarea {
    width: 100% !important;
    border-radius: 10px;
    border: 1px solid #333;
    background-color: #fff9c4;
    color: black;
}
.stButton > button {
    background-color: black;
    color: yellow;
    border: 1px solid #999;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
}
.stButton > button:hover {
    background-color: #333;
}
h1 {
    text-align: center;
    color: white;
    margin-top: 10px;
}
</style>
<div id="bg-animation"></div>
""", unsafe_allow_html=True)

# ===== Title =====
st.markdown("<h1>🤖 Fareaa's Chatbot</h1>", unsafe_allow_html=True)

# ===== Session Init =====
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to Fareaa's AI assistant, how can I help you today?"}]

# ===== Chat Display =====
st.markdown('<div id="chat-wrapper">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "bot"
    st.markdown(f'<div class="chat-box {role}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== Input Form =====
st.markdown('<div id="chat-input-wrapper">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("💬", placeholder="Enter your message here...", height=40, label_visibility="collapsed")
    submitted = st.form_submit_button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# ===== Submit Logic =====
if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Thinking..."):
        async def run_bot():
            return await Runner.run(
                starting_agent=agent,
                input=st.session_state.messages,
                run_config=config
            )

        try:
            result = asyncio.run(run_bot())
            reply = result.final_output
        except Exception as e:
            reply = f"❌ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
