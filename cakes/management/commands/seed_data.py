from django.core.management.base import BaseCommand
from cakes.models import Category, Cake
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial cake categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        categories = [
            'Birthday Cakes',
            'Wedding Cakes',
            'Cupcakes',
            'Chocolate Special',
            'Fruit Cakes'
        ]

        category_objects = {}
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            category_objects[cat_name] = cat
            if created:
                self.stdout.write(f'Created category: {cat_name}')

        cakes = [
            {
                'category': 'Birthday Cakes',
                'name': 'Classic Vanilla Birthday',
                'price': 25.00,
                'description': 'A fluffy vanilla sponge with buttercream frosting and sprinkles.'
            },
            {
                'category': 'Birthday Cakes',
                'name': 'Rainbow Surprise',
                'price': 45.00,
                'description': 'Six layers of vibrant colors with white chocolate ganache.'
            },
            {
                'category': 'Chocolate Special',
                'name': 'Double Chocolate Fudge',
                'price': 30.00,
                'description': 'Rich dark chocolate cake with chocolate fudge layers.'
            },
            {
                'category': 'Cupcakes',
                'name': 'Red Velvet Cupcake',
                'price': 3.50,
                'description': 'Individual red velvet cakes with cream cheese frosting.'
            },
            {
                'category': 'Wedding Cakes',
                'name': 'Elegant 3-Tier White',
                'price': 250.00,
                'description': 'A stunning three-tier cake decorated with edible lace and flowers.'
            }
        ]

        for cake_data in cakes:
            cake, created = Cake.objects.get_or_create(
                name=cake_data['name'],
                defaults={
                    'category': category_objects[cake_data['category']],
                    'slug': slugify(cake_data['name']),
                    'price': cake_data['price'],
                    'description': cake_data['description'],
                    'available': True
                }
            )
            if created:
                self.stdout.write(f'Created cake: {cake_data["name"]}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
