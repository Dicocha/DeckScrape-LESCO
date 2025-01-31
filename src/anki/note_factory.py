import genanki
import templates


class NoteFactory:
    @staticmethod
    async def create_note(word, filename):
        return genanki.Note(
            model=templates.MODEL_ID, fields=[word, f'<img src="{filename}">']
        )
