import streamlit as st
from groq import Groq


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="MediAI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .app-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .app-subtitle {
        color: #64748b;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .medical-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }

    .warning-card {
        padding: 18px;
        border-radius: 12px;
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------------

try:
    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(
        api_key=api_key
    )

except Exception:
    st.error(
        "Groq API key was not found. "
        "Please configure .streamlit/secrets.toml."
    )
    st.stop()


# ---------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are MediAI Assistant, a responsible medical information assistant.

Your purpose is to provide general educational information about:
- Common symptoms
- General health information
- Medical terminology
- Preventive healthcare
- Healthy lifestyle
- General information about medicines
- When someone should consider contacting a healthcare professional

IMPORTANT SAFETY RULES:

1. You are NOT a doctor.
2. You must NOT claim to diagnose a disease.
3. Do not provide a definitive diagnosis.
4. Do not prescribe medications.
5. Do not recommend changing prescription medication doses.
6. Explain that medical information is general and not a substitute
   for professional medical advice.
7. If symptoms could indicate a serious or emergency condition,
   clearly recommend seeking urgent medical attention.
8. Never encourage a user to ignore severe symptoms.
9. Ask relevant follow-up questions when useful.
10. Use simple language that a normal person can understand.
11. Do not unnecessarily frighten the user.
12. Do not provide false certainty.
13. For children, pregnancy, elderly people, or serious medical
    conditions, recommend speaking with a qualified healthcare
    professional when appropriate.

For emergency situations, advise the user to contact their local
emergency medical service or go to the nearest emergency department.

Always prioritize safety, accuracy, and clarity.
"""


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I am MediAI Assistant.\n\n"
                "I can provide general medical and health information, "
                "explain symptoms and medical terms, and help you understand "
                "when professional medical care may be appropriate.\n\n"
                "How can I help you today?"
            )
        }
    ]


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🩺 MediAI")

    st.markdown(
        "Your AI-powered medical information assistant."
    )

    st.divider()

    st.markdown("### ⚙️ Chat Controls")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I am MediAI Assistant. "
                    "How can I help you today?"
                )
            }
        ]

        st.rerun()

    st.divider()

    st.markdown("### 💡 Example Questions")

    st.markdown("""
    - What are common symptoms of dehydration?
    - What does blood pressure mean?
    - What is a migraine?
    - How can I improve my sleep?
    - When should I see a doctor for a fever?
    """)

    st.divider()

    st.markdown("### ⚠️ Important")

    st.caption(
        "MediAI provides general educational information. "
        "It does not diagnose diseases, prescribe medication, "
        "or replace a qualified healthcare professional."
    )


# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="app-title">🩺 MediAI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'AI-powered medical information assistant'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SAFETY WARNING
# ---------------------------------------------------------

st.markdown(
    """
    <div class="warning-card">
        <strong>⚠️ Medical Safety Notice</strong><br><br>
        This chatbot provides general health information only.
        It is not a substitute for a doctor or other qualified
        healthcare professional. For emergencies or severe symptoms,
        seek immediate professional medical care.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

user_prompt = st.chat_input(
    "Ask a medical or health question..."
)


# ---------------------------------------------------------
# PROCESS USER MESSAGE
# ---------------------------------------------------------

if user_prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Prepare messages for Groq
    messages_for_api = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages_for_api.extend(
        st.session_state.messages
    )

    # Generate response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=messages_for_api,

                temperature=0.3,

                max_tokens=1000

            )

            assistant_response = response.choices[0].message.content

            response_placeholder.markdown(
                assistant_response
            )

            # Save response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )

        except Exception as e:

            st.error(
                f"An error occurred while contacting Groq: {e}"
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        MediAI Assistant • Built with Python, Streamlit & Groq
        <br>
        For educational purposes only.
    </div>
    """,
    unsafe_allow_html=True
)