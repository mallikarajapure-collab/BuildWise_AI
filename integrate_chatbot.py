from pathlib import Path
import shutil

app_path = Path("app.py")
app = app_path.read_text(encoding="utf-8-sig")

marker = "# BUILDWISE CHATBOT INTERFACE"

if marker in app:
    print("Chatbot interface already exists. No duplicate added.")
else:
    backup = Path("app.py.before-chatbot")
    if not backup.exists():
        shutil.copy2(app_path, backup)

    old_import = "from services.recommender import recommend_projects"
    new_import = (
        old_import + "\n"
        "from services.llm_service import get_chatbot_response"
    )

    if old_import not in app:
        raise SystemExit(
            "Could not find the expected import. app.py was not changed."
        )

    app = app.replace(old_import, new_import, 1)

    chat_ui = '''

# BUILDWISE CHATBOT INTERFACE
st.divider()
st.subheader("💬 BuildWise AI — Project Mentor")
st.caption(
    "Ask about project ideas, skills, roadmaps, or internship preparation."
)

if "buildwise_chat_history" not in st.session_state:
    st.session_state["buildwise_chat_history"] = []

for chat_message in st.session_state["buildwise_chat_history"]:
    with st.chat_message(chat_message["role"]):
        st.write(chat_message["content"])

prompt = st.chat_input("Ask BuildWise AI a question...")

if prompt:
    st.session_state["buildwise_chat_history"].append(
        {"role": "user", "content": prompt}
    )

    answer = get_chatbot_response(prompt)

    st.session_state["buildwise_chat_history"].append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()
'''

    app = app.rstrip() + "\n" + chat_ui
    app_path.write_text(app, encoding="utf-8")
    print("SUCCESS: Chatbot interface added to app.py")
    print("Backup created: app.py.before-chatbot")
