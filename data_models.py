from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"Author(id={self.id!r}, name={self.name!r}, birth_date={self.birth_date!r}, date_of_death={self.date_of_death!r})"

    def __str__(self):
        death = self.date_of_death.year if self.date_of_death else "-"
        birth = self.birth_date.year if self.birth_date else "-"
        return f"{self.name} ({birth} - {death})"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True)
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author')

    def __repr__(self):
        return (f"Book(id={self.id!r}, isbn={self.isbn!r}, title={self.title!r}, "
                f"publication_year={self.publication_year!r}, "
                f"author_id={self.author_id!r})")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
