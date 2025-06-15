import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт CSV файла в соответствующую модель'

    def add_arguments(self, parser):
        parser.add_argument(
            'model',
            type=str,
            choices=['Category', 'Comment', 'Genre',
                     'GenreTitle', 'Review', 'Title', 'User']
        )
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        csv_file_path = options['csv_path']
        model_name = options['model']

        model_mapping = {
            'Category': Category,
            'Genre': Genre,
            'Title': Title,
            'GenreTitle': TitleGenre,
            'Review': Review,
            'Comment': Comment,
            'User': User,
        }

        model = model_mapping[model_name]

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_id = row.pop('category', None)
                if category_id:
                    category = Category.objects.get(id=category_id)
                    row['category'] = category
                author_id = row.pop('author', None)
                if author_id:
                    author = User.objects.get(id=author_id)
                    row['author'] = author
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'Модель {model_name} импортирована в БД из {csv_file_path}'))
