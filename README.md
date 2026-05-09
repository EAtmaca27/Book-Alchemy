# Book Alchemy

A personal library management web app built with Flask and SQLAlchemy. Add books and authors, browse your collection, and search or sort entries — all backed by a local SQLite database.

## Features

- **Browse your library** — view all books as cards with cover art fetched automatically from Open Library using the book's ISBN
- **Search** — filter books by title or author name
- **Sort** — sort the library by title or author name via a dropdown
- **Book detail page** — click any book card to see a full-size cover, ISBN, publication year, and author info
- **Add authors** — add an author with their name, birthdate, and optional date of death
- **Add books** — add a book with its title, ISBN, publication year, and a linked author
- **Delete books** — remove a book from the library; if the author has no remaining books, they are removed too

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** Jinja2 templates, plain CSS
- **Cover images:** [Open Library Covers API](https://openlibrary.org/dev/docs/api#anchor_covers)

## Project Structure

```
Book-Alchemy/
├── app.py               # Flask routes and app setup
├── data_models.py       # SQLAlchemy models (Author, Book)
├── data/
│   └── library.sqlite   # SQLite database
├── static/
│   ├── styles.css       # Global stylesheet
│   └── no_cover.png     # Fallback image for missing covers
└── templates/
    ├── base.html        # Shared layout with nav bar
    ├── home.html        # Library overview with search and sort
    ├── book_detail.html # Individual book detail page
    ├── add_book.html    # Form to add a new book
    └── add_author.html  # Form to add a new author
```

## Setup

1. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

2. **Create the database** — uncomment the `db.create_all()` block at the bottom of `app.py` for the first run, then comment it out again:
   ```python
   # in app.py __main__ block:
   with app.app_context():
       db.create_all()
   ```
   Alternatively, run it directly:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5002` in your browser.

## Usage

1. Go to **Add Author** and create at least one author before adding books.
2. Go to **Add Book**, fill in the details, and select the author.
3. The book will appear on the **Library** homepage with its cover loaded from Open Library.
4. Click a book card to view its detail page, or click **Delete** to remove it.
