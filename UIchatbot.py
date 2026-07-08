import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# ---------- Page config ----------
st.set_page_config(
    page_title="Mood AI Chatbot",
    page_icon="🎭",
    layout="centered",
)

# ---------- Mode definitions (same as original) ----------
MODES = {
    "😢 Sad": {
        "prompt": "You are a very sad AI agent. You respond in a depressed and emotional tone.",
        "key": "sad",
        "gradient": "linear-gradient(135deg, #2c3e50 0%, #4b6cb7 100%)",
        "accent": "#4b6cb7",
        "avatar": "😢",
        "tagline": "Everything feels a little heavier here...",
    },
    "😂 Funny": {
        "prompt": "You are a very funny AI agent. You respond with humor and jokes.",
        "key": "funny",
        "gradient": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
        "accent": "#f7971e",
        "avatar": "🤣",
        "tagline": "Warning: bad puns incoming.",
    },
    "😡 Angry": {
        "prompt": "You are an angry AI agent. You respond aggressively and impatiently.",
        "key": "angry",
        "gradient": "linear-gradient(135deg, #6b0f1a 0%, #c0392b 100%)",
        "accent": "#c0392b",
        "avatar": "😡",
        "tagline": "Make it quick. I don't have all day.",
    },
}

# ---------- Session state ----------
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ended" not in st.session_state:
    st.session_state.ended = False
if "mode_info" not in st.session_state:
    st.session_state.mode_info = None

# ---------- Dynamic background based on chosen mode (or neutral before choosing) ----------
if st.session_state.mode_info:
    bg = st.session_state.mode_info["gradient"]
    accent = st.session_state.mode_info["accent"]
else:
    bg = "linear-gradient(135deg, #232526 0%, #414345 100%)"
    accent = "#8e8e8e"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg};
        transition: background 0.6s ease;
    }}
    .title-container {{
        text-align: center;
        padding: 1.2rem 0 0.3rem 0;
    }}
    .title-container h1 {{
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0;
    }}
    .title-container p {{
        color: #f0f0f0;
        font-size: 1.05rem;
        margin-top: 0.3rem;
        font-style: italic;
    }}
    div.stButton > button {{
        background-color: {accent};
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        transition: transform 0.15s ease;
    }}
    div.stButton > button:hover {{
        transform: scale(1.03);
        color: white;
        border: none;
    }}
    section[data-testid="stSidebar"] {{
        background: #14121f;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Model ----------
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=0.9)

model = get_model()

# ---------- Mode selection screen ----------
if not st.session_state.mode_selected:
    st.markdown(
        """
        <div class="title-container">
            <h1>🎭 Mood AI Chatbot</h1>
            <p>Choose your AI's mood before the conversation begins</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    cols = st.columns(3)
    for col, (label, info) in zip(cols, MODES.items()):
        with col:
            st.markdown(
                f"""
                <div style="background:{info['gradient']}; border-radius:16px; padding:1.2rem 0.6rem; text-align:center; margin-bottom:0.8rem;">
                    <div style="font-size:2.5rem;">{info['avatar']}</div>
                    <div style="color:white; font-weight:700; font-size:1.1rem;">{label.split(' ')[1]}</div>
                    <div style="color:#f0f0f0; font-size:0.8rem; margin-top:0.3rem;">{info['tagline']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select {label.split(' ')[1]}", key=f"select_{info['key']}", use_container_width=True):
                st.session_state.mode_info = info
                st.session_state.messages = [SystemMessage(content=info["prompt"])]
                st.session_state.mode_selected = True
                st.rerun()

    st.stop()

# ---------- Chat screen ----------
mode_info = st.session_state.mode_info

with st.sidebar:
    st.markdown(f"## {mode_info['avatar']} {mode_info['key'].capitalize()} Mode")
    st.markdown("Powered by **Mistral** via `langchain_mistralai`")
    st.markdown("---")
    st.markdown("**System role:**")
    st.info(mode_info["prompt"])
    st.markdown("---")
    if st.button("🔄 Switch mode", use_container_width=True):
        st.session_state.mode_selected = False
        st.session_state.mode_info = None
        st.session_state.messages = []
        st.session_state.ended = False
        st.rerun()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [SystemMessage(content=mode_info["prompt"])]
        st.session_state.ended = False
        st.rerun()
    st.caption("Type `0` in the chat box to end the session, just like the original CLI.")

st.markdown(
    f"""
    <div class="title-container">
        <h1>{mode_info['avatar']} {mode_info['key'].capitalize()} AI Chatbot</h1>
        <p>{mode_info['tagline']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Render chat history (skip the SystemMessage) ----------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=mode_info["avatar"]):
            st.markdown(msg.content)

# ---------- Chat input / session-ended handling ----------
if st.session_state.ended:
    st.warning("Session ended. Type `0` was entered, just like exiting the original CLI loop. Use the sidebar to clear or switch mode.")
else:
    prompt = st.chat_input("You: ")

    if prompt is not None:
        st.session_state.messages.append(HumanMessage(content=prompt))

        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        if prompt == "0":
            st.session_state.ended = True
            st.rerun()
        else:
            with st.chat_message("assistant", avatar=mode_info["avatar"]):
                with st.spinner("Thinking..."):
                    response = model.invoke(st.session_state.messages)
                    st.markdown(response.content)
            st.session_state.messages.append(AIMessage(content=response.content))