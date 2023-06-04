import csv
import os
from django.core.management.base import BaseCommand

from reviews.models import (
    Genre,
    Category,
    Comment,
    Review,
    Title,
    GenreTitle,
)
from users.models import User


PATH_DATA = os.path.abspath('static/data') + '/'
FILES_CSV = {
    'category': PATH_DATA + 'category.csv',
    'genre': PATH_DATA + 'genre.csv',
    'user': PATH_DATA + 'users.csv',
    'genre_title': PATH_DATA + 'genre_title.csv',
    'title': PATH_DATA + 'titles.csv',
    'review': PATH_DATA + 'review.csv',
    'comment': PATH_DATA + 'comments.csv',
}
OPTIONS = {
    'category': ['category', 'title', 'review'],
    'genre': ['genre', 'title', 'review'],
    'user': ['user', 'review'],
    'title': ['title', 'review'],
    'review': ['review'],
}


def fill(create_model, path_file, CurrentModel=None):
    with open(path_file) as file_csv:
        reader = csv.DictReader(file_csv)
        try:
            for line in reader:
                create_model(line, CurrentModel)
        except Exception as error:
            print(error)


def fill_category_genre(line, CurrentModel):
    instance = CurrentModel(
        id=line['id'],
        name=line['name'],
        slug=line['slug'],
    )
    instance.save()


def fill_user(line, *args, **kwargs):
    instance = User(
        id=line['id'],
        username=line['username'],
        email=line['email'],
        role=line['role'],
        bio=line['bio'],
        first_name=line['first_name'],
        last_name=line['last_name'],
    )
    instance.save()


def fill_title(line, *args, **kwargs):
    instance = Title(
        id=line['id'],
        name=line['name'],
        year=line['year'],
        category=Category(id=line['category']),
    )
    instance.save()


def fill_genre_title(line, *args, **kwargs):
    instance = GenreTitle(
        id=line['id'],
        title_id=Title(id=line['title_id']),
        genre_id=Genre(id=line['genre_id']),
    )
    instance.save()


def fill_review(line, *args, **kwargs):
    instance = Review(
        id=line['id'],
        title_id=line['title_id'],
        text=line['text'],
        author=User(id=line['author']),
        score=line['score'],
        pub_date=line['pub_date'],
    )
    instance.save()


def fill_comment(line, *args, **kwargs):
    instance = Comment(
        id=line['id'],
        review_id=Review(id=line['review_id']),
        text=line['text'],
        author=User(id=line['author']),
        pub_date=line['pub_date'],
    )
    instance.save()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            action='store_true',
            help='Заполняет раздел "Категории" базы данных',
        )
        parser.add_argument(
            '--genre',
            action='store_true',
            help='Заполняет раздел "Жанры" базы данных',
        )
        parser.add_argument(
            '--user',
            action='store_true',
            help='Заполняет раздел "Пользователи" базы данных',
        )
        parser.add_argument(
            '--title',
            action='store_true',
            help=('Заполняет раздел "Произведения" базы данных, '
                  'также заполняются разделы "Категории", "Жанры" '
                  ' и "Произведения"'),
        )
        parser.add_argument(
            '--review',
            action='store_true',
            help=('Заполняет все разделы базы данных '
                  'кроме "Комментарии"'),
        )

    def handle(self, *args, **options):
        no_options = all(
            not options[option] for option in OPTIONS.keys())
        if any(
            options[option] for option in OPTIONS['category']
        ) or (no_options):
            fill(fill_category_genre, FILES_CSV['category'], Category)
        if any(
            options[option] for option in OPTIONS['genre']
        ) or no_options:
            fill(fill_category_genre, FILES_CSV['genre'], Genre)
        if any(
            options[option] for option in OPTIONS['user']
        ) or no_options:
            fill(fill_user, FILES_CSV['user'])
        if any(
            options[option] for option in OPTIONS['title']
        ) or no_options:
            fill(fill_title, FILES_CSV['title'])
            fill(fill_genre_title, FILES_CSV['genre_title'])
        if any(
            options[option] for option in OPTIONS['review']
        ) or no_options:
            fill(fill_review, FILES_CSV['review'])
        if no_options:
            fill(fill_comment, FILES_CSV['comment'])
