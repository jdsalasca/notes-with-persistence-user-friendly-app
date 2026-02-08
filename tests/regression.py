import unittest
import datetime
import uuid
import os
import json
import httpx # For testing API endpoints

from app import app # Import FastAPI app
from database import DummyLocalDatabase

# Use a different port for testing to avoid conflicts
TEST_PORT = 8001

class TestDummyLocalDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a fresh database instance for each test."""
        self.db = DummyLocalDatabase()
        notes = self.db.get_all_notes()
        if len(notes) >= 2:
            self.note1_id = notes[0]['id']
            self.note2_id = notes[1]['id']
        else:
            self.note1_id = None
            self.note2_id = None

    def test_initial_data_load(self):
        """Test that initial dummy data is loaded correctly."""
        notes = self.db.get_all_notes()
        self.assertEqual(len(notes), 2, "Should have 2 initial notes")
        self.assertIsInstance(notes[0], dict)
        self.assertIn('id', notes[0])
        self.assertIn('title', notes[0])
        self.assertIn('content', notes[0])
        self.assertIn('created_at', notes[0])
        self.assertIn('updated_at', notes[0])

    def test_create_note(self):
        """Test creating a new note."""
        new_note_data = {
            "id": str(uuid.uuid4()),
            "title": "Test Note",
            "content": "This is a test note content.",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        created_note = self.db.create_note(new_note_data)
        self.assertEqual(created_note, new_note_data)
        retrieved_note = self.db.get_note(new_note_data["id"])
        self.assertEqual(retrieved_note, new_note_data)

    def test_get_note(self):
        """Test retrieving a specific note."""
        if self.note1_id:
            note = self.db.get_note(self.note1_id)
            self.assertIsNotNone(note)
            self.assertEqual(note['id'], self.note1_id)
        else:
            self.skipTest("Initial notes not loaded properly")

    def test_get_all_notes(self):
        """Test retrieving all notes."""
        notes = self.db.get_all_notes()
        self.assertEqual(len(notes), 2)
        note_ids = [n['id'] for n in notes]
        self.assertIn(self.note1_id, note_ids)
        self.assertIn(self.note2_id, note_ids)

    def test_update_note(self):
        """Test updating an existing note."""
        if self.note1_id:
            update_data = {
                "title": "Updated Test Note Title",
                "content": "This is the updated content.",
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            updated_note = self.db.update_note(self.note1_id, update_data)
            self.assertIsNotNone(updated_note)
            self.assertEqual(updated_note['title'], "Updated Test Note Title")
            self.assertEqual(updated_note['content'], "This is the updated content.")
            self.assertEqual(updated_note['id'], self.note1_id)
            self.assertGreater(updated_note['updated_at'], self.db.get_note(self.note1_id)['created_at'])

            retrieved_note = self.db.get_note(self.note1_id)
            self.assertEqual(retrieved_note['title'], "Updated Test Note Title")
        else:
            self.skipTest("Initial notes not loaded properly")

    def test_update_nonexistent_note(self):
        """Test updating a note that does not exist."""
        nonexistent_id = str(uuid.uuid4())
        update_data = {
            "title": "Nonexistent",
            "content": "Should not be updated",
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        result = self.db.update_note(nonexistent_id, update_data)
        self.assertIsNone(result)

    def test_delete_note(self):
        """Test deleting an existing note."""
        if self.note1_id:
            deleted_note = self.db.delete_note(self.note1_id)
            self.assertIsNotNone(deleted_note)
            self.assertEqual(deleted_note['id'], self.note1_id)
            self.assertIsNone(self.db.get_note(self.note1_id))
            self.assertEqual(len(self.db.get_all_notes()), 1)
        else:
            self.skipTest("Initial notes not loaded properly")

    def test_delete_nonexistent_note(self):
        """Test deleting a note that does not exist."""
        nonexistent_id = str(uuid.uuid4())
        result = self.db.delete_note(nonexistent_id)
        self.assertIsNone(result)

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the FastAPI app."""
        self.client = httpx.AsyncClient(app=app, base_url=f"http://localhost:{TEST_PORT}")
        # Reset the dummy database before each test to ensure isolation
        # A more robust approach would be to mock the db instance used by the app
        # For simplicity here, we'll re-initialize it.
        # This requires a way to access the db instance from the app.
        # Assuming `db` in `app.py` is the instance we can access.
        # In a real app, you'd use dependency injection.
        from app import db # This might fail if app is not imported correctly
        db._notes = {}
        db._initialize_dummy_data()

    def tearDown(self):
        """Close the test client."""
        self.client.close()

    async def asyncSetUp(self):
        await self.setUp()

    async def asyncTearDown(self):
        await self.tearDown()

    # --- Test API Endpoints ---

    def test_create_note_api(self):
        """Test creating a note via the API."""
        response = self.client.post("/notes", json={"title": "API Test", "content": "Content for API test."})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "API Test")
        self.assertEqual(data["content"], "Content for API test.")

    def test_create_note_missing_fields_api(self):
        """Test creating a note with missing fields."""
        response = self.client.post("/notes", json={"title": "API Test"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_get_notes_api(self):
        """Test retrieving all notes via the API."""
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, 200)
        notes = response.json()
        self.assertIsInstance(notes, list)
        self.assertTrue(len(notes) >= 2) # Should have initial notes

    def test_get_note_api(self):
        """Test retrieving a single note via the API."""
        # Get an existing note ID from dummy data
        response_all = self.client.get("/notes")
        self.assertEqual(response_all.status_code, 200)
        initial_notes = response_all.json()
        note_id_to_get = initial_notes[0]['id']

        response = self.client.get(f"/notes/{note_id_to_get}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], note_id_to_get)

    def test_get_nonexistent_note_api(self):
        """Test retrieving a non-existent note."""
        nonexistent_id = "a1b2c3d4-e5f6-7890-1234-567890abcdeff"
        response = self.client.get(f"/notes/{nonexistent_id}")
        self.assertEqual(response.status_code, 404)

    def test_update_note_api(self):
        """Test updating a note via the API."""
        # Get an existing note ID
        response_all = self.client.get("/notes")
        self.assertEqual(response_all.status_code, 200)
        initial_notes = response_all.json()
        note_id_to_update = initial_notes[0]['id']

        update_data = {
            "title": "API Updated Title",
            "content": "API Updated Content."
        }
        response = self.client.put(f"/notes/{note_id_to_update}", json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], note_id_to_update)
        self.assertEqual(data["title"], "API Updated Title")
        self.assertEqual(data["content"], "API Updated Content.")
        # Check if updated_at has changed
        self.assertNotEqual(data['created_at'], data['updated_at'])

    def test_update_nonexistent_note_api(self):
        """Test updating a non-existent note."""
        nonexistent_id = "a1b2c3d4-e5f6-7890-1234-567890abcdeff"
        update_data = {
            "title": "API Updated Title",
            "content": "API Updated Content."
        }
        response = self.client.put(f"/notes/{nonexistent_id}", json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_note_api(self):
        """Test deleting a note via the API."""
        # Get an existing note ID
        response_all = self.client.get("/notes")
        self.assertEqual(response_all.status_code, 200)
        initial_notes = response_all.json()
        note_id_to_delete = initial_notes[0]['id']

        response = self.client.delete(f"/notes/{note_id_to_delete}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], note_id_to_delete)

        # Verify it's actually deleted by trying to get it
        get_response = self.client.get(f"/notes/{note_id_to_delete}")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_nonexistent_note_api(self):
        """Test deleting a non-existent note."""
        nonexistent_id = "a1b2c3d4-e5f6-7890-1234-567890abcdeff"
        response = self.client.delete(f"/notes/{nonexistent_id}")
        self.assertEqual(response.status_code, 404)

    def test_root_path_returns_html(self):
        """Test that the root path serves index.html."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')
        # Basic check for expected content
        self.assertIn(b'<title>Notes App</title>', response.content)


if __name__ == '__main__':
    # To run API tests, you need to run uvicorn separately or use an ASGI test client.
    # For simplicity, we are using httpx's test client which directly loads the app.
    # Running `python -m unittest tests/regression.py` should work.
    unittest.main()
