import asyncio
import time

from src.anki.deck_builder import DeckBuilder
from src.utils.data_manager import DataManager
from src.scraping.scraper import WebScraper


BASE_URL = "https://academiaaprendecr.com/diccionariolesco/"


async def main():
    start_time = time.time()
    data_manager = DataManager()

    scraper = WebScraper(BASE_URL, data_manager)

    # Start scraping
    await scraper.scrape()

    # Instantiate the AnkiDeckBuilder
    builder = DeckBuilder()

    # Add cards from the scraped data
    builder.add_cards(data_manager.get_data())

    builder.save_deck()

    print(f"\n\nMy program took {round(time.time() - start_time, 2)} to run")


if __name__ == "__main__":
    asyncio.run(main())
