# 🗣️ Feedback Collection Platform (Python + FastAPI + Streamlit)

A full-stack mini project where **admins (businesses)** can create feedback forms and view responses, while **users (customers)** can submit feedback anonymously via a public link.

---

## 💡 Features

### Admin (Business)
- Register & Login (JWT-based authentication)
- Create feedback forms with 3–5 customizable questions (text or multiple choice)
- View responses in a basic dashboard (raw text answers)

### Customer (User)
- Access feedback form via public link (Form ID)
- Submit answers without login

---

## 🛠 Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Backend     | Python, FastAPI     |
| Frontend    | Streamlit           |
| Database    | SQLite + SQLAlchemy |
| Auth        | JWT (OAuth2)        |

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

git clone https://github.com/your-username/feedback-platform.git
cd feedback-platform

### 2. Create Virtual Environment & Install Dependencies

    python -m venv venv
    venv\Scripts\activate  # On Windows
    # or
    source venv/bin/activate  # On Mac/Linux

    pip install -r requirements.txt

    Start Backend (FastAPI)
    uvicorn backend.main:app --reload
    Visit: http://localhost:8000/docs (Swagger UI)

    Start Frontend (Streamlit)
    streamlit run frontend/app.py
    Visit: http://localhost:8501

    🧪 1. Test via Swagger (FastAPI) Visit the interactive API docs:📍 http://localhost:8000/docs

        ✅ Test Flow
        Register an admin
        POST /register
        ➤ Use a valid email + password

        Login to get JWT token
        POST /token
        ➤ Copy the access_token from response

        Create a feedback form
        POST /forms/
        ➤ Use your token as Bearer <token> in the Authorize section
        ➤ Provide title + 3–5 questions (text/mcq)

        Submit feedback anonymously
        POST /submit/{form_id}
        ➤ Fill out answers (as public user)

        View responses
        GET /forms/{form_id}/responses
        ➤ Admin-only (requires token)


    🧪 2. Test via Streamlit UI
        Run the UI: streamlit run frontend/app.py

            Frontend Pages to Test:
            ✅ Login / Register: Admin can create an account

            ✅ Create Form: Add a new feedback form

            ✅ Copy Public Link: Use generated form ID

            ✅ Public User Page: Submit answers (no login)

```bash