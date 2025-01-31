import genanki


from utils.async_manager import AsyncManager
from utils.file_manager import FileManager
from anki.deck_manager import DeckManager
from anki.note_factory import NoteFactory


class DeckBuilder:
    def __init__(self, media_dir="media"):
        self.file_manager = FileManager()
        self.deck_manager = DeckManager()
        self.async_manager = AsyncManager()
        self.deck = self.deck_manager.get_deck()
        self.media_dir = media_dir
        self.data = []  # Store data for media files

    async def add_cards(self, data):
        """
        Adds cards to the deck asynchronously.
        :param data: A list of dictionaries with 'word' and 'file_path'.
        """
        try:
            # Process all notes asynchronously
            notes = await self.async_manager.process_tasks(
                [
                    NoteFactory.create_note(
                        entry["word"], entry["file_path"], self.model
                    )
                    for entry in data
                ]
            )

            # Add all generated notes to the deck
            for note in notes:
                self.deck.add_note(note)

            # Store media file paths
            self.data.extend(entry["file_path"] for entry in data)

        except Exception as e:
            print(f"Failed to add cards. Error: {e}")

    def save_deck(self, file_name="Lesco.apkg"):
        """
        Saves the deck to a file.
        :param file_name: Name of the output file.
        """
        try:
            package = genanki.Package(self.deck)
            package.media_files = self.data  # Correct reference to media files
            package.write_to_file(file_name)
            print(f"Deck saved successfully as {file_name}")
        except Exception as e:
            print(f"Failed to save deck: {e}")
