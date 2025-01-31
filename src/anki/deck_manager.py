import random
import genanki


class DeckManager:
    _instance = None

    def __new__(cls, name="Lesco Deck"):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.deck = genanki.Deck(
                deck_id=random.randrange(1 << 30, 1 << 31), name=name
            )
        return cls._instance

    def get_deck(self):
        return self.deck
