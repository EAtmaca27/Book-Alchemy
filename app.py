import os

from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.secret_key = 'dev'
db.init_app(app)


@app.route('/')
def index():
    sort = request.args.get('sort', 'title')
    query = request.args.get('query', '')

    books_q = Book.query.join(Book.author)
    if query:
        books_q = books_q.filter(
            Book.title.ilike(f'%{query}%') | Author.name.ilike(f'%{query}%')
        )

    if sort == 'author':
        books_q = books_q.order_by(Author.name)
    else:
        books_q = books_q.order_by(Book.title)

    books = books_q.all()
    return render_template('home.html', books=books, sort=sort, query=query)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        death_str = request.form.get('date_of_death')
        date_of_death = datetime.strptime(death_str, '%Y-%m-%d').date() if death_str else None

        author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author
    title = book.title

    db.session.delete(book)
    db.session.commit()

    if not Book.query.filter_by(author_id=author.id).first():
        db.session.delete(author)
        db.session.commit()
        flash(f'"{title}" and its author were deleted from the library.')
    else:
        flash(f'"{title}" was successfully deleted from the library.')

    return redirect(url_for('index'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('add_book'))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


if __name__ == '__main__':
    # Uncomment to create the database tables on first run
    # Delete database file to reset the database
    # Delete following 2 lines to avoid creating tables on every run
    # or keep them commented out
    '''with app.app_context():
        db.create_all()'''

    app.run()
