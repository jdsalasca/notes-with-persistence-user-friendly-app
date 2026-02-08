# DummyLocal Adapters Documentation

This document describes the `DummyLocal` adapters used in the project. These adapters simulate interactions with external services (like databases, queues, or external APIs) for local development, ensuring the application can run without requiring actual external infrastructure.

## Purpose

The primary goal of `DummyLocal` adapters is to enable full local executability of the application. They mock the behavior of real-world services, allowing developers to test core application logic without complex setup or reliance on external systems.

## Current Implementations

### 1. `DummyLocalDatabase` (in `database.py`)

- **Simulates:** A relational database (conceptually similar to PostgreSQL).
- **Persistence:** Uses an in-memory dictionary (`self._notes`) to store data. Data is lost when the application restarts.
- **Features:** Implements basic CRUD (Create, Read, Update, Delete) operations for a 'Note' entity.
  - `create_note(note_data)`: Adds a new note.
  - `get_note(note_id)`: Retrieves a single note by its ID.
  - `get_all_notes()`: Retrieves all notes, sorted by `created_at`.
  - `update_note(note_id, update_data)`: Updates an existing note's fields and `updated_at` timestamp.
  - `delete_note(note_id)`: Removes a note by its ID.
- **Initialization:** Includes sample dummy data upon instantiation to provide an immediate working state.
- **Constraints:** Basic checks for required fields are handled at the API layer, not within the dummy adapter itself (mimicking how a real DB might rely on application logic for validation).

## How to Extend

To add new `DummyLocal` adapters:

1.  **Create a new class** in a dedicated file (e.g., `integrations.py`) or within the `database.py` file if closely related.
2.  **Mimic the interface** of the real service you are simulating. For example, if simulating an AWS SQS queue, create methods like `send_message`, `receive_message`, `delete_message`.
3.  **Implement the logic** using Python's standard libraries (e.g., in-memory lists/dictionaries, file I/O for simple file-based persistence, `datetime`, `uuid`).
4.  **Update the main application code** to import and use your new `DummyLocal` adapter instead of any real service clients.

## Example: Simulating a Queue

If you needed a `DummyLocalQueue`:

```python
import collections

class DummyLocalQueue:
    def __init__(self):
        self._queue = collections.deque()

    def send_message(self, message_body):
        self._queue.append(message_body)
        print(f"[DummyLocalQueue] Sent: {message_body}")

    def receive_message(self):
        if not self._queue:
            return None
        message = self._queue.popleft()
        print(f"[DummyLocalQueue] Received: {message}")
        return {"Body": message}

    def delete_message(self, receipt_handle):
        # In-memory deque doesn't need explicit handles for this simple simulation
        print(f"[DummyLocalQueue] Deleted message (handle: {receipt_handle})")
        return True
```
