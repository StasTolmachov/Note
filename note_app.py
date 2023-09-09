import json
import os
import datetime

class Note:
    def __init__(self, title, body):
        self.id = None
        self.title = title
        self.body = body
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp
        }

class NoteApp:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
            notes = []
            for item in data:
                note = Note(item["title"], item["body"])
                note.id = item["id"]
                note.timestamp = item["timestamp"]
                notes.append(note)
            return notes
        return []

    def save_notes(self):
        with open(self.filename, "w") as f:
            json.dump([note.to_dict() for note in self.notes], f)

    def add_note(self, title, body):
        note = Note(title, body)
        note.id = len(self.notes) + 1
        self.notes.append(note)
        self.save_notes()

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def edit_note(self, note_id, new_title=None, new_body=None):
        for note in self.notes:
            if note.id == note_id:
                if new_title:
                    note.title = new_title
                if new_body:
                    note.body = new_body
                note.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_notes()

    def view_notes(self):
        for note in self.notes:
            print(f"ID: {note.id}\nTitle: {note.title}\nBody: {note.body}\nTimestamp: {note.timestamp}\n")

if __name__ == "__main__":
    app = NoteApp()
    while True:
        print("1. View Notes")
        print("2. Add Note")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            app.view_notes()
        elif choice == "2":
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            app.add_note(title, body)
        elif choice == "3":
            note_id = int(input("Enter note ID to edit: "))
            new_title = input("Enter new title (or leave blank): ")
            new_body = input("Enter new body (or leave blank): ")
            app.edit_note(note_id, new_title if new_title else None, new_body if new_body else None)
        elif choice == "4":
            note_id = int(input("Enter note ID to delete: "))
            app.delete_note(note_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
