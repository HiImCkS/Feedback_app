import streamlit as st
import requests
# import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Feedback App", layout="centered")

st.title("📝 Feedback Collection Platform")

menu = ["Public Feedback", "Admin Panel"]
choice = st.sidebar.radio("Choose mode", menu)

# ------------------------------
# PUBLIC: Submit Feedback Form
# ------------------------------
if choice == "Public Feedback":
    form_id = st.text_input("Enter Form ID to submit feedback")
    if form_id:
        res = requests.get(f"{API_URL}/forms/{form_id}")
        if res.status_code == 200:
            data = res.json()
            st.subheader(data['title'])

            answers = []
            for q in data['questions']:
                if q['type'] == 'text':
                    ans = st.text_input(q['text'])
                elif q['type'] == 'mcq':
                    ans = st.radio(q['text'], q['options'])
                else:
                    ans = ""
                answers.append({"question_id": q['id'], "answer": ans})

            if st.button("Submit Feedback"):
                submit = requests.post(f"{API_URL}/forms/{form_id}/submit", json={"answers": answers})
                if submit.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                else:
                    st.error("❌ Submission failed.")
        else:
            st.warning("Form not found.")

# ------------------------------
# ADMIN PANEL
# ------------------------------
elif choice == "Admin Panel":
    if "token" not in st.session_state:
        with st.form("login"):
            st.subheader("🔐 Admin Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                res = requests.post(f"{API_URL}/token", json={"email": email, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.success("Login successful")
                else:
                    st.error("Invalid credentials")

    if "token" in st.session_state:
        tab = st.selectbox("Choose admin task", ["Create Form", "View Responses", "Logout"])
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        if tab == "Create Form":
            st.subheader("🛠️ Create Feedback Form")
            title = st.text_input("Form Title")
            num_qs = st.number_input("How many questions?", min_value=1, max_value=10, value=3)

            questions = []
            for i in range(num_qs):
                st.markdown(f"#### Question {i+1}")
                q_text = st.text_input(f"Text for question {i+1}", key=f"qtext{i}")
                q_type = st.selectbox("Type", ["text", "mcq"], key=f"qtype{i}")
                options = ""
                if q_type == "mcq":
                    options = st.text_input("Options (comma separated)", key=f"opts{i}")
                questions.append({
                    "question_text": q_text,
                    "question_type": q_type,
                    "options": options
                })

            if st.button("Create"):
                form_data = {"title": title, "questions": questions}
                res = requests.post(f"{API_URL}/forms", json=form_data, headers=headers)
                if res.status_code == 200:
                    st.success(f"Form created! Form ID: {res.json()['form_id']}")
                else:
                    st.error("Failed to create form")

        elif tab == "View Responses":
            st.subheader("📊 View Responses")
            form_id = st.text_input("Enter your Form ID")
            if st.button("Fetch Responses"):
                res = requests.get(f"{API_URL}/forms/{form_id}/responses", headers=headers)
                if res.status_code == 200:
                    all_responses = res.json()
                    st.success(f"Total Responses: {len(all_responses)}")
                    for i, r in enumerate(all_responses):
                        st.markdown(f"##### Response #{i+1}")
                        for ans in r:
                            st.write(f"Q{ans['question_id']}: {ans['answer']}")
                        st.markdown("---")
                else:
                    st.error("Couldn't fetch responses")

        elif tab == "Logout":
            del st.session_state.token
            st.success("Logged out")
