
import streamlit as st
from services.recommender import recommend_projects
from services.llm_service import get_chatbot_response

st.set_page_config(
    page_title="BuildWise AI",
    page_icon="🚀",
    layout="wide"
)

# Premium UI theme — existing application logic remains unchanged
from pathlib import Path as _ThemePath
_theme_css = _ThemePath("style.css")
if _theme_css.exists():
    st.markdown(
        "<style>" + _theme_css.read_text(encoding="utf-8-sig") + "</style>",
        unsafe_allow_html=True,
    )

PROJECTS = [
    {
        "name": "Smart Study Planner",
        "level": "Beginner",
        "category": "Productivity",
        "time": "1–2 weeks",
        "skills": ["Python", "Streamlit", "Basic Logic"],
        "description": "Create a study schedule based on subjects, deadlines and available study hours.",
        "steps": [
            "Build a form for subjects and deadlines",
            "Create a simple study scheduling algorithm",
            "Display the schedule in a dashboard",
            "Add progress tracking"
        ]
    },
    {
        "name": "Job Application Tracker",
        "level": "Intermediate",
        "category": "Career",
        "time": "2–3 weeks",
        "skills": ["Python", "SQLite", "Streamlit"],
        "description": "Track job applications, interview stages, deadlines and application status.",
        "steps": [
            "Design the application data model",
            "Store applications in SQLite",
            "Build add, edit and search features",
            "Create application statistics"
        ]
    },
    {
        "name": "ML Model Performance Auditor",
        "level": "Advanced",
        "category": "AI / ML",
        "time": "3–5 weeks",
        "skills": ["Python", "Pandas", "Scikit-learn", "ML"],
        "description": "Inspect model evaluation results and flag possible data leakage or suspicious metrics.",
        "steps": [
            "Load a sample machine-learning dataset",
            "Create a train/test evaluation workflow",
            "Check for suspicious evaluation patterns",
            "Generate an evidence-based audit report"
        ]
    },
    {
        "name": "GitHub Portfolio Analyzer",
        "level": "Intermediate",
        "category": "Developer Tools",
        "time": "2–4 weeks",
        "skills": ["Python", "REST API", "GitHub API"],
        "description": "Analyze public GitHub repositories and identify strengths and areas for improvement.",
        "steps": [
            "Collect public GitHub profile data",
            "Analyze repository descriptions and activity",
            "Create a transparent scoring system",
            "Generate a portfolio improvement roadmap"
        ]
    },
    {
        "name": "AI Document Question Answering",
        "level": "Advanced",
        "category": "Generative AI",
        "time": "3–5 weeks",
        "skills": ["Python", "LLMs", "Embeddings", "Vector Search"],
        "description": "Build a document assistant that answers questions using information from uploaded documents.",
        "steps": [
            "Allow users to upload documents",
            "Extract and split document text",
            "Retrieve relevant passages for a question",
            "Generate answers grounded in retrieved content"
        ]
    },
    {
        "name": "Personal Expense Dashboard",
        "level": "Beginner",
        "category": "Data Analytics",
        "time": "1–2 weeks",
        "skills": ["Python", "Pandas", "Data Visualization"],
        "description": "Explore spending patterns through categories, monthly totals and charts.",
        "steps": [
            "Create an expense entry form",
            "Store expenses in a dataset",
            "Calculate totals by category",
            "Display spending charts"
        ]
    }
]

st.markdown(
    "<h1 style='text-align:center;'>🚀 BuildWise AI</h1>"
    "<p style='text-align:center;'>Discover a project that moves your career forward.</p>",
    unsafe_allow_html=True
)

st.divider()

st.subheader("🎯 Tell us about your goals")

left, right = st.columns(2)

with left:
    interests = st.multiselect(
        "Which areas interest you?",
        ["AI / ML", "Generative AI", "Career", "Productivity",
         "Developer Tools", "Data Analytics"],
        default=["AI / ML", "Generative AI"]
    )
    level = st.selectbox(
        "Your current coding level",
        ["Beginner", "Intermediate", "Advanced"]
    )

with right:
    goal = st.selectbox(
        "Your main goal",
        ["Get an internship", "Build a portfolio",
         "Learn a new skill", "Prepare for placements"]
    )
    available_time = st.selectbox(
        "Time available",
        ["1–2 weeks", "2–3 weeks", "3–5 weeks", "Any"]
    )

skills = st.multiselect(
    "Skills you already know (optional)",
    ["Python", "Java", "SQL", "Pandas", "Streamlit",
     "REST API", "GitHub API", "Scikit-learn", "LLMs"],
    help="Choose the skills you have already practised."
)

if st.button("✨ Discover My Projects", type="primary", use_container_width=True):
    level_order = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    user_level = level_order[level]
    results = []

    for project in PROJECTS:
        if level_order[project["level"]] > user_level:
            continue

        if available_time != "Any" and project["time"] != available_time:
            continue

        interest_match = (
            not interests
            or project["category"] in interests
            or (project["category"] == "Generative AI" and "AI / ML" in interests)
        )

        if interest_match:
            results.append(project)

    if not results:
        results = [
            p for p in PROJECTS
            if level_order[p["level"]] <= user_level
        ]

    results.sort(
        key=lambda p: sum(skill in skills for skill in p["skills"]),
        reverse=True
    )

    st.session_state["results"] = results
    st.session_state["goal"] = goal
    st.session_state["skills"] = skills

if "results" in st.session_state:
    st.divider()
    st.subheader("🧭 Your Project Recommendations")
    st.caption(
        "Recommendations are generated using project rules and your selected preferences. "
        "Live LLM recommendations are not connected yet."
    )

    for index, project in enumerate(st.session_state["results"], start=1):
        with st.container(border=True):
            st.markdown(f"### {index}. {project['name']}")
            a, b, c = st.columns(3)
            a.metric("Difficulty", project["level"])
            b.metric("Estimated time", project["time"])
            c.metric("Career fit", st.session_state["goal"])

            st.write(project["description"])
            st.markdown("**Skills involved:** " + ", ".join(project["skills"]))

            user_skills = st.session_state["skills"]
            missing = [s for s in project["skills"] if s not in user_skills]

            if missing:
                st.info("Skills to learn or practise: " + ", ".join(missing))
            else:
                st.success("Your selected skills match this project's skill list!")

            with st.expander("🗺️ View step-by-step roadmap"):
                for step_number, step in enumerate(project["steps"], start=1):
                    st.write(f"{step_number}. {step}")

st.divider()
st.caption("BuildWise AI • Project Discovery MVP • Rule-based recommendations")


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
