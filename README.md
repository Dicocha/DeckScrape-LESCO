# 📚 Anki Card Generator (Lesco Dictionary)

This project scrapes data from a **Lesco dictionary**, processes it into an **Anki deck**, and exports it as a `.apkg` file for learning.

## 🚀 Features
- 🖥 **Web Scraping**: Extracts words and videos from `academiaaprendecr.com`.
- 🎴 **Anki Deck Generator**: Uses `genanki` to generate flashcards.
- ⚡ **Async Processing**: Speeds up card creation using `asyncio`.
- 🛠 **Error Handling**: Logs errors to `error.log`.

## 📦 Installation
1. **Clone the repository:**
   ```sh
   git clone [https://github.com/Dicocha/DeckScrape-LESCO.git]
   cd anki-card-generator

2. **Active venv:**
`python -m venv venv`
`source venv/bin/activate`  # On Windows: venv\Scripts\activate

3. **Install requirements**
`pip install -r requirements.txt`
