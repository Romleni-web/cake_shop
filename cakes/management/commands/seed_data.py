from django.core.management.base import BaseCommand
from cakes.models import Category, Cake
from django.utils.text import slugify
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Seeds the database with initial cake categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Default Admin if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@melanincakehouse.com', 'MelaninAdmin2024')
            self.stdout.write(self.style.SUCCESS('Created default superuser: admin'))

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
                'price': 2500.00,
                'description': 'A fluffy vanilla sponge with buttercream frosting and sprinkles.',
                'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500'
            },
            {
                'category': 'Birthday Cakes',
                'name': 'Rainbow Surprise',
                'price': 4500.00,
                'description': 'Six layers of vibrant colors with white chocolate ganache.',
                'image_url': 'https://images.unsplash.com/photo-1535141192574-5d4897c12636?w=500'
            },
            {
                'category': 'Chocolate Special',
                'name': 'Double Chocolate Fudge',
                'price': 3000.00,
                'description': 'Rich dark chocolate cake with chocolate fudge layers.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500'
            },
            {
                'category': 'Cupcakes',
                'name': 'Red Velvet Cupcake',
                'price': 350.00,
                'description': 'Individual red velvet cakes with cream cheese frosting.',
                'image_url': 'https://images.unsplash.com/photo-1614707267537-b85af00c4b81?w=500'
            },
            {
                'category': 'Wedding Cakes',
                'name': 'Elegant 3-Tier White',
                'price': 25000.00,
                'description': 'A stunning three-tier cake decorated with edible lace and flowers.',
                'image_url': 'https://images.unsplash.com/photo-1522673607200-16488321499b?w=500'
            }
        ]

        # Note: In a real app with FileField, we'd need to download the image.
        # For this quick fix, we'll keep the image field empty but I'll update
        # the template to show these Unsplash images as defaults.

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
