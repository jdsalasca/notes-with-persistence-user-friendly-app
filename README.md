# Notes App

A production-lean starter application for a notes app with persistence and a user-friendly UX.

## Features
- Create, view, edit, and delete notes.
- Persistence using a simulated local database.
- User-friendly interface.

## Local Development Setup

This application is designed to run entirely locally without external dependencies. It uses **DummyLocal adapters** to simulate interactions with databases, external APIs, and queues.

### Prerequisites
- Python 3.7+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd autopilot-create-a-notes-app-20260208
    ```

2.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn python-dotenv
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
    ```
    The server will run on `http://localhost:8000`.

2.  **Access the application:**
    Open your web browser and navigate to:
    `http://localhost:8000`

### Database Strategy

The application uses a `DummyLocalDatabase` class located in `database.py`. This class simulates a relational database (like PostgreSQL) by storing data in memory. For development purposes, this is sufficient and requires no external database setup.

**Schema Definition:**
- The conceptual schema is defined in `schemas.md`.
- A sample SQL schema for PostgreSQL is provided in `db/schema.sql` for reference.

### Development Notes
- **Frontend:** The frontend is a simple HTML, CSS, and JavaScript application served statically.
- **Backend:** The backend is built with FastAPI, providing RESTful API endpoints for note management.
- **DummyLocal Adapters:** All external service integrations (database, etc.) are mocked using `DummyLocal` classes to ensure local execution without setup.

## Project Structure
```
.
├── .gitignore          # Specifies intentionally untracked files
├── README.md           # This file
├── app.py              # Main FastAPI application
├── database.py         # DummyLocal database adapter
├── schemas.md          # Schema documentation
├── db/
│   └── schema.sql      # Sample SQL schema
├── public/
│   ├── index.html      # Main HTML page
│   ├── style.css       # CSS for styling
│   └── script.js       # JavaScript for frontend logic
├── tests/
│   ├── regression.py   # Regression tests
│   └── regression_notes.md # Notes on regression tests
├── docs/
│   └── dummy_local_docs.md # Documentation for DummyLocal adapters
└── requirements.txt    # Project dependencies (optional, but good practice)
```

## Regression Tests

Regression tests are located in `tests/regression.py`. They verify the functionality of the `DummyLocalDatabase` and the API endpoints.

## Documentation

- **Schema:** `schemas.md`
- **Local DB Strategy:** This README file.
- **DummyLocal Adapters:** `docs/dummy_local_docs.md`
