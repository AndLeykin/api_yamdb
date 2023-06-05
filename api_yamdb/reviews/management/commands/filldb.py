import csv
import os
from traceback import print_exc
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
FIELDS_FOR_ID = ['category', 'author']


def fill(path_file, CurrentModel):
    with open(path_file) as file_csv:
        instance = CurrentModel()
        try:
            first_line = file_csv.readline().strip('\n')
            keys = first_line.split(',')
            file_csv.seek(0)
            reader = csv.DictReader(file_csv)
            for line in reader:
                for key in keys:
                    if key in FIELDS_FOR_ID:
                        model_field = key + '_id'
                    else:
                        model_field = key
                    setattr(instance, model_field, line[key])
                instance.save()
        except Exception:
            print_exc()
            exit()
    print('Перенесены данные из файла', path_file)


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
                  'также заполняются разделы "Категории" и "Жанры"'),
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
            fill(FILES_CSV['category'], Category)
        if any(
            options[option] for option in OPTIONS['genre']
        ) or no_options:
            fill(FILES_CSV['genre'], Genre)
        if any(
            options[option] for option in OPTIONS['user']
        ) or no_options:
            fill(FILES_CSV['user'], User)
        if any(
            options[option] for option in OPTIONS['title']
        ) or no_options:
            fill(FILES_CSV['title'], Title)
            fill(FILES_CSV['genre_title'], GenreTitle)
        if any(
            options[option] for option in OPTIONS['review']
        ) or no_options:
            fill(FILES_CSV['review'], Review)
        if no_options:
            fill(FILES_CSV['comment'], Comment)
