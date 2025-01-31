import random
from typing import List, Dict
import threading


class DataManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._data: List[Dict[str, str]] = []
            self._words: List[str] = []
            self._urls: List[str] = []
            self._initialized = True

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance of DataManager."""
        return cls()

    @property
    def data(self) -> List[Dict[str, str]]:
        """Returns the current list of data entries."""
        return self._data

    @property
    def words(self) -> List[str]:
        """Returns the current list of words."""
        return self._words

    @property
    def urls(self) -> List[str]:
        """Returns the current list of URLs."""
        return self._urls

    def add_data(self, word: str, file_path: str) -> None:
        """
        Adds a new entry (word and file path) to the data manager.
        :param word: The word to add.
        :param file_path: The file path to associate with the word.
        """
        self._data.append({"word": word, "file_path": file_path})

    def add_word(self, word: str) -> None:
        """Adds a word to the words list."""
        self._words.append(word)

    def add_url(self, url: str) -> None:
        """Adds a URL to the URLs list."""
        self._urls.append(url)

    def verify_length(self) -> bool:
        """
        Verifies if the length of the words list matches the URLs list.
        :return: True if lengths match, False otherwise.
        """
        return len(self._words) == len(self._urls)

    def shuffle_data(self) -> None:
        """
        Shuffles the order of the data list.
        :return: None
        """
        random.shuffle(self._data)
