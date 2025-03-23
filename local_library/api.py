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