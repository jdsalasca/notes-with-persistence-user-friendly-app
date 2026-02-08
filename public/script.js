document.addEventListener('DOMContentLoaded', () => {
    const noteTitleInput = document.getElementById('note-title');
    const noteContentInput = document.getElementById('note-content');
    const saveNoteBtn = document.getElementById('save-note-btn');
    const notesContainer = document.getElementById('notes-container');

    // --- Helper Functions ---

    function formatTimestamp(isoString) {
        if (!isoString) return '';
        const date = new Date(isoString);
        return date.toLocaleString(); // e.g., "2/8/2026, 10:30:00 AM"
    }

    function renderNote(note) {
        const noteElement = document.createElement('li');
        noteElement.classList.add('note-item');
        noteElement.dataset.id = note.id;

        noteElement.innerHTML = `
            <div class="note-item-header">
                <h3>${escapeHtml(note.title)}</h3>
                <div class="note-item-actions">
                    <button class="edit-btn">Edit</button>
                    <button class="delete-btn">Delete</button>
                </div>
            </div>
            <div class="note-item-content">${escapeHtml(note.content)}</div>
            <div class="note-item-timestamp">
                Created: ${formatTimestamp(note.created_at)} | Updated: ${formatTimestamp(note.updated_at)}
            </div>
        `;

        noteElement.querySelector('.edit-btn').addEventListener('click', () => editNote(note));
        noteElement.querySelector('.delete-btn').addEventListener('click', () => deleteNote(note.id));

        return noteElement;
    }

    async function loadNotes() {
        try {
            const response = await fetch('/notes');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const notes = await response.json();
            notesContainer.innerHTML = ''; // Clear existing notes
            notes.forEach(note => {
                notesContainer.appendChild(renderNote(note));
            });
        } catch (error) {
            console.error("Error loading notes:", error);
            notesContainer.innerHTML = '<li class="error">Failed to load notes. Please try again later.</li>';
        }
    }

    async function createNote() {
        const title = noteTitleInput.value.trim();
        const content = noteContentInput.value.trim();

        if (!title || !content) {
            alert('Please enter both title and content for the note.');
            return;
        }

        try {
            const response = await fetch('/notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, content }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
            }

            const newNote = await response.json();
            notesContainer.prepend(renderNote(newNote));

            noteTitleInput.value = '';
            noteContentInput.value = '';
            alert('Note saved successfully!');
        } catch (error) {
            console.error("Error creating note:", error);
            alert(`Failed to save note: ${error.message}`);
        }
    }

    function editNote(note) {
        noteTitleInput.value = note.title;
        noteContentInput.value = note.content;

        saveNoteBtn.textContent = 'Update Note';
        saveNoteBtn.onclick = async () => {
            const updatedTitle = noteTitleInput.value.trim();
            const updatedContent = noteContentInput.value.trim();

            if (!updatedTitle || !updatedContent) {
                alert('Please enter both title and content for the note.');
                return;
            }

            try {
                const response = await fetch(`/notes/${note.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title: updatedTitle, content: updatedContent }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
                }

                const updatedNote = await response.json();
                const noteElement = notesContainer.querySelector(`.note-item[data-id="${note.id}"]`);
                if (noteElement) {
                    const newNoteElement = renderNote(updatedNote);
                    notesContainer.replaceChild(newNoteElement, noteElement);
                }

                noteTitleInput.value = '';
                noteContentInput.value = '';
                saveNoteBtn.textContent = 'Save Note';
                saveNoteBtn.onclick = createNote; 
                alert('Note updated successfully!');

            } catch (error) {
                console.error("Error updating note:", error);
                alert(`Failed to update note: ${error.message}`);
            }
        };
    }

    async function deleteNote(noteId) {
        if (!confirm('Are you sure you want to delete this note?')) {
            return;
        }

        try {
            const response = await fetch(`/notes/${noteId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
            }

            const noteElement = notesContainer.querySelector(`.note-item[data-id="${noteId}"]`);
            if (noteElement) {
                noteElement.remove();
            }
            alert('Note deleted successfully!');
        } catch (error) {
            console.error("Error deleting note:", error);
            alert(`Failed to delete note: ${error.message}`);
        }
    }

    function escapeHtml(unsafe) {
        if (typeof unsafe !== 'string') return unsafe;
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    // --- Event Listeners ---

    saveNoteBtn.addEventListener('click', createNote);

    loadNotes();
});
