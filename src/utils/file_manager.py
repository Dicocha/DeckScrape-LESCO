import mimetypes
import os
from urllib.parse import urlsplit

from utils.data_manager import DataManager


class FileManager:
    def __init__(self):
        self.data_manager = DataManager.get_instance()

    @staticmethod
    def get_file_extension(url):
        """
        Extracts or guesses the file extension from a URL.
        :param url: The URL to analyze.
        :return: The file extension as a string.
        """
        path = urlsplit(url).path
        file_extension = os.path.splitext(path)[-1].lower()

        if not file_extension:  # If no extension in URL, attempt to guess it
            guessed_type, _ = mimetypes.guess_type(url)
            file_extension = mimetypes.guess_extension(guessed_type) or ""

        return file_extension

    @staticmethod
    def construct_file_path(download_dir, word, file_extension):
        """
        Constructs the file path for the downloaded file.
        :param download_dir: The directory to save the file.
        :param word: The associated word for the file.
        :param file_extension: The file extension to use.
        :return: The complete file path as a string.
        """
        filename = f"{word}{file_extension}"
        return os.path.join(download_dir, filename)

    @staticmethod
    def extract_filename(file_path):
        """
        Extracts the filename from a file path.
        :param file_path: The full path of the file.
        :return: The filename (e.g., "example.webp").
        """
        return os.path.basename(file_path)

    @staticmethod
    def extract_word(filename):
        """
        Extract the word from the filename
        :return: Word sanitized
        """
        word, _ = os.path.splitext(filename)
        return word.strip()

    def extract_words_from_filenames(self, media_folder="media/"):
        """
        Extract words from all filenames in the 'media/' folder and add them to the DataManager.
        :return: Word and filepath in tuple
        """

        for filename in os.listdir(media_folder):
            # Ignore non-files
            file_path = os.path.join(media_folder, filename)
            if not os.path.isfile(file_path):
                continue

            # Add the entry to the DataManager
            return (self.extract_word(filename), file_path)
