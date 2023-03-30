# recipes/management/commands/load_data_ingr.py

import os

from csv import reader
from django.core.management import BaseCommand, CommandError

from foodgram import settings
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        path_to_data = os.path.join(
            settings.BASE_DIR.resolve().parent.parent, 'data'
        )
        file = os.path.join(path_to_data, 'ingredients.csv')
        print('Start import data')
        # file = f'{path_to_data}/ingredients.csv'
        try:
            with open(file, encoding='utf-8') as f:
                for ingredient in reader(f):
                    Ingredient.objects.get_or_create(
                        name=ingredient[0],
                        measurement_unit=ingredient[1],
                    )
            print('End of import data')
        except FileNotFoundError:
            raise CommandError(f'Файл ingredients.csv не найден в {file}')
