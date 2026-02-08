# Architecture

This document outlines the architecture of the Notes Application.

## Overview

The Notes Application is a simple web-based application designed for creating, managing, and persisting user notes. It prioritizes a user-friendly interface and reliable data storage.

## Components

### Frontend

-   **Technology:** HTML, CSS, JavaScript.
-   **Purpose:** Provides the user interface for interacting with the application. This includes displaying notes, forms for creating/editing notes, and user feedback.
-   **User Experience:** Designed to be intuitive and responsive, ensuring a seamless user experience for note-taking.

### Backend

-   **Technology:** Python (`app.py`).
-   **Purpose:** Acts as the server-side application logic. It handles incoming requests from the frontend, processes them, and interacts with the database.
-   **API:** Likely exposes a RESTful API for CRUD (Create, Read, Update, Delete) operations on notes.

### Database

-   **Technology:** SQL database (e.g., SQLite, PostgreSQL, as managed by `database.py` and defined in `db/schema.sql`).
-   **Purpose:** Provides persistence for all user notes. Ensures that notes are saved and available even after the application is restarted.
-   **Schema:** Defined in `db/schema.sql`, outlining the structure for storing note content, timestamps, and potentially other metadata.

## Data Flow

1.  User interacts with the frontend (e.g., clicks 'Save Note').
2.  The frontend JavaScript sends an HTTP request to the backend API.
3.  The Python backend (`app.py`) receives the request.
4.  The backend uses `database.py` to interact with the SQL database (e.g., insert, update, or retrieve notes).
5.  The database stores or provides the requested data.
6.  The backend sends a response back to the frontend.
7.  The frontend updates the UI based on the response.

## Key Features

-   **Note Creation:** Users can create new text-based notes.
-   **Note Editing:** Existing notes can be modified.
-   **Note Deletion:** Users can remove notes.
-   **Persistence:** All notes are stored reliably in the database.
-   **User-Friendly Interface:** A clean and intuitive UI for easy note management.
