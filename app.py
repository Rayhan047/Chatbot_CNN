from pathlib import Path
from utils.chatbot import predict, get_action
from datetime import datetime
from textwrap import dedent

import base64
import uuid
import streamlit as st
import time
import html
import re


CURRENT_DIR = Path(__file__).parent

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_path = CURRENT_DIR / "assets" / "logo_umsu.png"
logo_base64 = get_base64_image(logo_path)

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Nova AI",
    page_icon="🤖",
    layout="centered",
)

# ======================================================
# CSS
# ======================================================

st.markdown(
    dedent(
        f"""
        <style>
        .stApp {{
            background: #0E1117;
        }}

        .stApp::before {{
            content:"";

            position:fixed;

            top:0;
            left:0;

            width:100vw;
            height:100vh;

            background-image:url("data:image/png;base64,{logo_base64}");

            background-repeat:no-repeat;

            background-position: 57% center;

            background-size:600px;

            opacity:0.05;

            pointer-events:none;

            z-index:0;
        }}

        .main {{
            position:relative;
            z-index:1;
        }}

        .nova-header {{
            text-align: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }}

        .nova-logo {{
            width: 90px;
            height: 90px;
            margin: auto;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563EB, #3B82F6);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 45px;
            color: white;
            box-shadow: 0 0 30px rgba(37,99,235,.35);
        }}

        .nova-title {{
            color: white;
            font-size: 36px;
            font-weight: 700;
            margin-top: 18px;
        }}

        .nova-subtitle {{
            color: #9CA3AF;
            font-size: 16px;
            margin-top: 6px;
        }}

        section[data-testid="stSidebar"] {{
            background: #161B22;
            border-right: 1px solid rgba(255,255,255,.08);
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {{
            color: white;
        }}

        .stButton>button {{
            width: 100%;
            border-radius: 12px;
        }}

        .stChatInputContainer {{
            border-top: none;
            background: #0E1117;
            padding-top: 12px;
        }}

        .dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #9CA3AF;
            animation: bounce 0.8s infinite;
        }}

        .dot:nth-child(2) {{
            animation-delay: .2s;
        }}

        .dot:nth-child(3) {{
            animation-delay: .4s;
        }}

        @keyframes bounce {{
            0% {{
                transform: translateY(0);
                opacity: .4;
            }}
            50% {{
                transform: translateY(-7px);
                opacity: 1;
            }}
            100% {{
                transform: translateY(0);
                opacity: .4;
            }}
        }}

        .user-row {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-end;
            gap: 10px;
            margin: 16px 0;
        }}

        .bot-row {{
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            gap: 10px;
            margin: 16px 0;
        }}

        .user-avatar,
        .bot-avatar {{
            width: 42px;
            height: 42px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 22px;
            flex-shrink: 0;
        }}

        .user-avatar {{
            background: #374151;
        }}

        .bot-avatar {{
            background: linear-gradient(135deg, #2563EB, #3B82F6);
            color: white;
            box-shadow: 0 0 12px rgba(37,99,235,.35);
        }}

        .user-bubble,
        .bot-bubble {{
            max-width: 72%;
            word-break: break-word;
            padding: 14px 18px;
            border-radius: 18px;
        }}

        .user-bubble {{
            background: #2563EB;
            color: white;
            border-bottom-right-radius: 6px;
            box-shadow: 0 4px 12px rgba(37,99,235,.25);
        }}

        .bot-bubble {{
            background: #1F2937;
            color: white;
            border-bottom-left-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,.25);
        }}

        /* ===========================
        History Card
        =========================== */

        .history-card {{
            background:#1F2937;
            border:1px solid rgba(255,255,255,.06);
            border-radius:14px;
            padding:14px 16px;
            margin-bottom:12px;
            cursor:pointer;
            transition:all .25s ease;
        }}

        .history-card:hover {{
            background:#273548;
            border:1px solid #3B82F6;
            transform:translateY(-2px);
            box-shadow:0 4px 12px rgba(59,130,246,.20);
        }}

        .history-title {{
            color:white;
            font-size:15px;
            font-weight:600;
            margin-bottom:6px;
        }}

        .history-date{{
            color:#9CA3AF;
            font-size:12px;
        }}

        .bot-title {{
            font-weight: bold;
            color: #60A5FA;
            margin-bottom: 8px;
        }}

        .chat-time {{
            font-size: 11px;
            margin-top: 8px;
            color: #9CA3AF;
        }}

        .chat-time-user {{
            text-align: right;
            color: #D1D5DB;
        }}
        </style>
        """
    ).strip(),
    unsafe_allow_html=True,
)

# ======================================================
# HELPER
# ======================================================

def get_time() -> str:
    return datetime.now().strftime("%H:%M")


def welcome_message() -> dict:
    return {
        "id": uuid.uuid4().hex,
        "role": "assistant",
        "content": {
            "title": "Selamat Datang 👋",
            "answer": "Halo! Saya Nova AI, Asisten Virtual FIKTI UMSU. Ada yang bisa saya bantu hari ini?",
            "button": None,
        },
        "time": get_time(),
    }

    def typewriter_text(text, placeholder, delay=0.03):
        shown = ""
        words = text.split()

    for word in words:
        if shown:
            shown += " "
        shown += word
        placeholder.markdown(shown)
        time.sleep(delay)


def typing_animation() -> None:
    st.markdown(
        dedent(
            """
            <div class="bot-row">
                <div class="bot-avatar">🤖</div>
                <div class="bot-bubble" style="display:flex; gap:6px; align-items:center; padding:18px 22px;">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

def typing_effect(title, answer, chat_time, button=None):

    placeholder = st.empty()

    current_text = ""

    words = answer.split()

    for word in words:

        if current_text:
            current_text += " "

        current_text += word

        with placeholder.container():

            bot_message(
                title,
                current_text,
                chat_time
            )

        time.sleep(0.08)

    placeholder.empty()

    bot_message(
        title,
        answer,
        chat_time
    )

    render_buttons(
        button,
        len(st.session_state.messages)
    )


def user_message(text: str, chat_time: str) -> None:
    safe_text = html.escape(text).replace("\n", "<br>")
    st.markdown(
        dedent(
            f"""
            <div class="user-row">
                <div class="user-bubble">
                    <div>{safe_text}</div>
                    <div class="chat-time chat-time-user">{html.escape(chat_time)}</div>
                </div>
                <div class="user-avatar">👤</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def bot_message(title, answer, chat_time):

    safe_title = html.escape(title)
    safe_answer = html.escape(answer).replace("\n", "<br>")

    st.markdown(
        dedent(
            f"""
            <div class="bot-row">
                <div class="bot-avatar">🤖</div>
                <div class="bot-bubble">
                    <div class="bot-title">{safe_title}</div>
                    <div>{safe_answer}</div>
                    <div class="chat-time">{html.escape(chat_time)}</div>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

def render_buttons(button, message_id):

    if not button:
        return

    cols = st.columns(len(button))

    for i, item in enumerate(button):

        with cols[i]:

            if "url" in item:

                st.link_button(
                    item["text"],
                    item["url"]
                )

            elif "action" in item:

                if st.button(
                    item["text"],
                    key=f"{item['action']}_{message_id}"
                ):

                    hasil = get_action(item["action"])

                    current_time = get_time()

                    st.session_state.messages.append(
                        {
                            "id": uuid.uuid4().hex,
                            "role": "assistant",
                            "content": hasil,
                            "time": current_time,
                        }
                    )

                    st.rerun()

def history_card(chat, index):

    text = f"💬 {chat['title']}\n🕒 {chat['date']} • {chat['time']}"

    return st.button(

        text,

        key=f"history_{index}",

        use_container_width=True

    )

# ======================================================
# HEADER
# ======================================================

st.markdown(
    dedent(
        """
        <div class="nova-header">
            <div class="nova-logo">🤖</div>
            <div class="nova-title">Nova AI</div>
            <div class="nova-subtitle">Asisten Virtual FIKTI UMSU</div>
        </div>
        """
    ).strip(),
    unsafe_allow_html=True,
)

# ======================================================
# SESSION CHAT
# ======================================================

if "messages" not in st.session_state:
    st.session_state.messages = [welcome_message()]

if "sidebar_mode" not in st.session_state:
    st.session_state.sidebar_mode = "home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    if st.session_state.sidebar_mode == "home":

        st.markdown("## 🤖 Nova AI")
        st.caption("Asisten Virtual FIKTI UMSU")
        st.divider()

        col1, col2, col3 = st.columns([1, 6, 1])

        with col2:
            if st.button("Percakapan Baru", use_container_width=True):

                st.session_state.messages = [welcome_message()]

                st.session_state.current_chat_index = None

                st.rerun()

        col1, col2, col3 = st.columns([1, 6, 1])

        with col2:
            if st.button("Riwayat Percakapan", use_container_width=True):

                st.session_state.sidebar_mode = "history"
                st.rerun()

        st.divider()
        st.markdown("### Informasi")
        st.write("**Model**")
        st.caption("CNN + Word2Vec")
        st.write("**Versi**")
        st.caption("Nova AI 1.0")
        st.write("**Developer**")
        st.caption("Rayhan Pratama")

    elif st.session_state.sidebar_mode == "history":

        if st.button("⬅ Kembali"):

            st.session_state.sidebar_mode = "home"

            st.rerun()

        st.divider()

        st.markdown("""
        <h2 style="
            text-align:center;
            color:white;
            margin-bottom:0;
        ">
        Riwayat
        </h2>
        """, unsafe_allow_html=True)

        st.markdown("""
            <p style="
                text-align:center;
                color:#9CA3AF;
                font-size:14px;
                margin-top:4px;
                margin-bottom:15px;
            ">
            Percakapan Anda
            </p>
            """, unsafe_allow_html=True)

        if len(st.session_state.chat_history) == 0:

            st.info("Belum ada riwayat percakapan.")

        else:

            for index in reversed(range(len(st.session_state.chat_history))):

                chat = st.session_state.chat_history[index]

                col_chat, col_delete = st.columns([8, 1])

                with col_chat:

                    if history_card(chat, index):

                        st.session_state.current_chat_index = index

                        st.session_state.messages = chat["messages"].copy()

                        st.session_state.sidebar_mode = "home"

                        st.rerun()

                with col_delete:

                    if st.button(

                        "✕",

                        key=f"delete_{index}"

                    ):

                        del st.session_state.chat_history[index]

                        # Jika chat yang sedang dibuka ikut dihapus
                        if st.session_state.current_chat_index == index:

                            st.session_state.current_chat_index = None
                            st.session_state.messages = [
                                welcome_message()
                            ]

                        # Kalau index menjadi tidak valid
                        elif (
                            st.session_state.current_chat_index is not None
                            and st.session_state.current_chat_index > index
                        ):

                            st.session_state.current_chat_index -= 1

                        st.rerun()

# ======================================================
# MENAMPILKAN RIWAYAT CHAT
# ======================================================

for idx, message in enumerate(st.session_state.messages):

    if message["role"] == "user":

        user_message(
            message["content"],
            message["time"]
        )

    else:

        bot_message(
            message["content"]["title"],
            message["content"]["answer"],
            message["time"],
        )

        render_buttons(
            message["content"].get("button"),
            message["id"]
        )

# ======================================================
# INPUT CHAT
# ======================================================

prompt = st.chat_input("Tulis pertanyaan...")

if prompt:
    current_time = get_time()

    # ==========================================
    # Membuat chat baru jika belum ada
    # ==========================================

    if st.session_state.current_chat_index is None:

        title = " ".join(prompt.split()[:5])

        if len(prompt.split()) > 5:
            title += "..."

        new_chat = {
            "title": title,
            "date": datetime.now().strftime("%d %b %Y"),
            "time": current_time,
            "messages": []
        }

        st.session_state.chat_history.append(new_chat)

        st.session_state.current_chat_index = len(st.session_state.chat_history) - 1


    # Simpan Pesan dari user
    #---------------------------

    st.session_state.messages.append(
        {
            "id": uuid.uuid4().hex,
            "role": "user",
            "content": prompt,
            "time": current_time,
        }
    )

    st.session_state.chat_history[
        st.session_state.current_chat_index
    ]["messages"] = st.session_state.messages.copy()

    user_message(prompt, current_time)

    typing_box = st.empty()
    with typing_box.container():
        typing_animation()

    time.sleep(1.0)
    hasil = predict(prompt)
    typing_box.empty()

    typing_effect(
        hasil["title"],
        hasil["answer"],
        current_time,
        hasil.get("button"),
    )

    st.session_state.messages.append(
        {
            "id": uuid.uuid4().hex,
            "role": "assistant",
            "content": hasil,
            "time": current_time,
        }
    )

    st.session_state.chat_history[
        st.session_state.current_chat_index
    ]["messages"] = st.session_state.messages.copy()


    st.rerun()
