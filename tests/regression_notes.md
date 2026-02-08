# Regression Test Notes

## Test Suite: `tests/regression.py`

This suite covers the core functionalities of the Notes application, ensuring stability and correctness.

### Test Categories:

1.  **DummyLocalDatabase Tests (`TestDummyLocalDatabase`)**
    - **Purpose:** Verifies the internal logic of the `DummyLocalDatabase` class, which simulates persistence.
    - **Coverage:** 
        - Initial data loading.
        - Creating new notes.
        - Retrieving single notes by ID.
        - Retrieving all notes.
        - Updating existing notes (verifying content and `updated_at` timestamp).
        - Attempting to update non-existent notes.
        - Deleting existing notes.
        - Attempting to delete non-existent notes.
    - **Notes:** These tests ensure the simulated persistence layer behaves as expected before interacting with the API.

2.  **API Endpoint Tests (`TestApiEndpoints`)**
    - **Purpose:** Verifies that the FastAPI application correctly handles HTTP requests and interacts with the `DummyLocalDatabase`.
    - **Coverage:** 
        - **POST /notes:** Creating notes (success and failure cases).
        - **GET /notes:** Retrieving all notes.
        - **GET /notes/{note_id}:** Retrieving a specific note (success and non-existent cases).
        - **PUT /notes/{note_id}:** Updating a note (success and non-existent cases, verifying `updated_at` change).
        - **DELETE /notes/{note_id}:** Deleting a note (success and non-existent cases).
        - **GET /:** Verifies the root path serves the `index.html` file correctly.
    - **Notes:** These tests use `httpx.AsyncClient` to simulate HTTP requests to the FastAPI application, ensuring the API contract is met and data consistency is maintained.

### Execution

Tests can be run using Python's built-in `unittest` module:

```bash
python -m unittest tests/regression.py
```

### Future Enhancements

- Add tests for frontend JavaScript interactions if a more complex frontend framework were used.
- Integrate with a Dockerized PostgreSQL instance for more realistic database testing, moving away from `DummyLocal` for this specific test category.
- Implement load testing or performance tests for API endpoints.
