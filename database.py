import datetime
import uuid
from typing import List, Dict, Any, Optional

class DummyLocalDatabase:
    def __init__(self):
        self._notes: Dict[str, Dict[str, Any]] = {}
        self._initialize_dummy_data()

    def _initialize_dummy_data(self):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        sample_note_id1 = str(uuid.uuid4())
        sample_note_id2 = str(uuid.uuid4())

        self._notes[sample_note_id1] = {
            "id": sample_note_id1,
            "title": "First Note",
            "content": "This is the content of the first note. It's a great day for coding!",
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        self._notes[sample_note_id2] = {
            "id": sample_note_id2,
            "title": "Second Note",
            "content": "Remember to buy groceries later.",
            "created_at": timestamp,
            "updated_at": timestamp,
        }

    def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        note_id = note_data["id"]
        self._notes[note_id] = note_data
        return note_data

    def get_note(self, note_id: str) -> Optional[Dict[str, Any]]:
        return self._notes.get(note_id)

    def get_all_notes(self) -> List[Dict[str, Any]]:
        # Return sorted by created_at for a better UX
        return sorted(self._notes.values(), key=lambda x: x.get("created_at", ""), reverse=True)

    def update_note(self, note_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if note_id not in self._notes:
            return None
        
        existing_note = self._notes[note_id]
        updated_note = existing_note.copy()
        updated_note.update(update_data)
        
        self._notes[note_id] = updated_note
        return updated_note

    def delete_note(self, note_id: str) -> Optional[Dict[str, Any]]:
        if note_id in self._notes:
            return self._notes.pop(note_id)
        return None
