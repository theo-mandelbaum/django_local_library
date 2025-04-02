from ninja import NinjaAPI, Schema, UploadedFile, File
from django.shortcuts import get_object_or_404

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"

@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}

class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user

# Create api endpoints for all CRUD actions for the Author model
from datetime import date
from catalog.models import Author

class AuthorIn(Schema):
    first_name: str
    last_name: str
    date_of_birth: date = None
    date_of_death: date = None

@api.post("/author/create")
def create_author(request, payload: AuthorIn):
    author = Author.objects.create(**payload.dict())
    return {"id": author.id}

class AuthorOut(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date = None
    date_of_death: date = None

@api.get("/author/{author_id}", response=AuthorOut)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

@api.put("/author/{author_id}")
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.delete("/author/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}


# Create api endpoints for all CRUD actions for Genre model
from catalog.models import Genre

class GenreIn(Schema):
    name: str

@api.post("/genre/create")
def create_genre(request, payload: GenreIn):
    genre = Genre.objects.create(**payload.dict())
    return {"id": genre.id}

class GenreOut(Schema):
    id: int
    name: str

@api.get("/genre/{genre_id}", response=GenreOut)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    return genre

@api.put("/genre/{genre_id}")
def update_genre(request, genre_id: int, payload: GenreIn):
    genre = get_object_or_404(Genre, id=genre_id)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

@api.delete("/genre/{genre_id}")
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    return {"success": True}


# Create api endpoints for all CRUD actions for Language model
from catalog.models import Language

class LanguageIn(Schema):
    name: str

@api.post("/language/create")
def create_language(request, payload: LanguageIn):
    language = Language.objects.create(**payload.dict())
    return {"id": language.id}

class LanguageOut(Schema):
    id: int
    name: str

@api.get("/language/{language_id}", response=LanguageOut)
def get_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    return language

@api.put("/language/{language_id}")
def update_language(request, language_id: int, payload: LanguageIn):
    language = get_object_or_404(Language, id=language_id)
    for attr, value in payload.dict().items():
        setattr(language, attr, value)
    language.save()
    return {"success": True}

@api.delete("/language/{language_id}")
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}

from catalog.models import Book, BookInstance
from typing import List
from django.conf import settings
from datetime import date

# Create Schemas

class BookIn(Schema):
    title: str
    author_id: int
    summary: str
    isbn: str
    genre_ids: List[int]

class BookOut(Schema):
    id: int
    title: str
    author: str
    summary: str
    isbn: str
    genre: List[str]

class BookInstanceIn(Schema):
    book_id: int
    imprint: str
    due_back: str
    borrower_id: int = None
    status: str

class BookInstanceOut(Schema):
    id: str
    book_id: int
    imprint: str
    due_back: str
    borrower_id: int = None
    status: str
    is_overdue: bool

# CRUD operations for Book

@api.post("/book/create", response=BookOut)
def create_book(request, payload: BookIn):
    author = get_object_or_404(Author, id=payload.author_id)
    genres = Genre.objects.filter(id__in=payload.genre_ids)
    book = Book.objects.create(
        title=payload.title,
        author=author,
        summary=payload.summary,
        isbn=payload.isbn,
    )
    book.genre.set(genres)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "summary": book.summary,
        "isbn": book.isbn,
        "genre": [genre.name for genre in book.genre.all()],
    }

@api.get("/book/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "summary": book.summary,
        "isbn": book.isbn,
        "genre": [genre.name for genre in book.genre.all()],
    }

@api.put("/book/{book_id}", response=BookOut)
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    author = get_object_or_404(Author, id=payload.author_id)
    genres = Genre.objects.filter(id__in=payload.genre_ids)
    book.title = payload.title
    book.author = author
    book.summary = payload.summary
    book.isbn = payload.isbn
    book.genre.set(genres)
    book.save()
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "summary": book.summary,
        "isbn": book.isbn,
        "genre": [genre.name for genre in book.genre.all()],
    }

@api.delete("/book/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}

# CRUD operations for BookInstance

@api.post("/book_instance/create", response=BookInstanceOut)
def create_book_instance(request, payload: BookInstanceIn):
    book = get_object_or_404(Book, id=payload.book_id)
    borrower = None
    if payload.borrower_id:
        borrower = get_object_or_404(settings.AUTH_USER_MODEL, id=payload.borrower_id)
    book_instance = BookInstance.objects.create(
        book=book,
        imprint=payload.imprint,
        due_back=payload.due_back,
        borrower=borrower,
        status=payload.status,
    )
    return {
        "id": book_instance.id,
        "book_id": book_instance.book.id,
        "imprint": book_instance.imprint,
        "due_back": book_instance.due_back,
        "borrower_id": book_instance.borrower.id if book_instance.borrower else None,
        "status": book_instance.status,
        "is_overdue": book_instance.is_overdue,
    }

@api.get("/book_instance/{book_instance_id}", response=BookInstanceOut)
def get_book_instance(request, book_instance_id: str):
    book_instance = get_object_or_404(BookInstance, id=book_instance_id)
    return {
        "id": book_instance.id,
        "book_id": book_instance.book.id,
        "imprint": book_instance.imprint,
        "due_back": book_instance.due_back,
        "borrower_id": book_instance.borrower.id if book_instance.borrower else None,
        "status": book_instance.status,
        "is_overdue": book_instance.is_overdue,
    }

@api.put("/book_instance/{book_instance_id}", response=BookInstanceOut)
def update_book_instance(request, book_instance_id: str, payload: BookInstanceIn):
    book_instance = get_object_or_404(BookInstance, id=book_instance_id)
    book = get_object_or_404(Book, id=payload.book_id)
    borrower = None
    if payload.borrower_id:
        borrower = get_object_or_404(settings.AUTH_USER_MODEL, id=payload.borrower_id)
    book_instance.book = book
    book_instance.imprint = payload.imprint
    book_instance.due_back = payload.due_back
    book_instance.borrower = borrower
    book_instance.status = payload.status
    book_instance.save()
    return {
        "id": book_instance.id,
        "book_id": book_instance.book.id,
        "imprint": book_instance.imprint,
        "due_back": book_instance.due_back,
        "borrower_id": book_instance.borrower.id if book_instance.borrower else None,
        "status": book_instance.status,
        "is_overdue": book_instance.is_overdue,
    }

@api.delete("/book_instance/{book_instance_id}")
def delete_book_instance(request, book_instance_id: str):
    book_instance = get_object_or_404(BookInstance, id=book_instance_id)
    book_instance.delete()
    return {"success": True}
