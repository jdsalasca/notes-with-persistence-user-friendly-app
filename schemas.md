# Notes App Schema

This document outlines the schema for the Notes application.

## Entities

### Note
Represents a single note entry.

#### Fields
- **id**: `UUID` (String representation)
    - Description: Unique identifier for the note.
    - Constraints: Primary Key, Not Null.
- **title**: `String`
    - Description: The title of the note.
    - Constraints: Not Null, Max Length (e.g., 255 characters).
- **content**: `String`
    - Description: The main body content of the note.
    - Constraints: Not Null.
- **created_at**: `DateTime` (ISO 8601 Format String)
    - Description: Timestamp when the note was created.
    - Constraints: Not Null.
- **updated_at**: `DateTime` (ISO 8601 Format String)
    - Description: Timestamp when the note was last updated.
    - Constraints: Not Null.

#### Relations
None for this simple application.

## Constraints Summary

- **Note.id**: Primary Key
- **Note.title**: Not Null
- **Note.content**: Not Null
- **Note.created_at**: Not Null
- **Note.updated_at**: Not Null
