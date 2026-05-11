import random
import uuid
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from faker import Faker

from core.models import SiteSettings, FAQ, Testimonial, Event, GalleryImage
from accounts.models import CustomUser
from destinations.models import Destination, DestinationImage, DestinationReview
from tours.models import TourCategory, TourPackage, TourImage, TourItinerary, TourReview
from hotels.models import Hotel, HotelImage, Room
from bookings.models import Booking
from contact.models import ContactMessage, OfficeLocation
from blogs.models import BlogCategory, BlogPost

User = get_user_model()
fake = Faker(['en_US'])

class Command(BaseCommand):
    help = 'Seed the database with realistic Bangladesh tourism data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning existing data...')
        Booking.objects.all().delete()
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()
        ContactMessage.objects.all().delete()
        OfficeLocation.objects.all().delete()
        Event.objects.all().delete()
        Testimonial.objects.all().delete()
        FAQ.objects.all().delete()
        Room.objects.all().delete()
        Hotel.objects.all().delete()
        TourPackage.objects.all().delete()
        TourCategory.objects.all().delete()
        Destination.objects.all().delete()
        # Keep admin users but delete random customers
        User.objects.filter(role='customer').delete()

        self.stdout.write('Seeding data...')
        
        # 1. Site Settings
        SiteSettings.objects.get_or_create(pk=1, defaults={
            'site_name': 'Adventure Bangladesh',
            'tagline': 'Explore the Pristine Beauty of the Delta',
            'email': 'tourism@adventurebangladesh.com',
            'phone': '+880 1711-223344',
            'address': 'Level 5, Tropical Diamond Tower, Gulshan-2, Dhaka 1212',
            'facebook': 'https://facebook.com/adventurebd',
            'instagram': 'https://instagram.com/adventurebd',
            'about_text': 'Adventure Bangladesh is a premier travel agency dedicated to providing authentic and sustainable travel experiences across the beautiful landscape of Bangladesh.',
        })

        # 2. Demo Users
        users = [
            ('imran_admin', 'imran@adventure.com', 'Imran@123', 'Imran Mahmud', 'superadmin'),
            ('eva_manager', 'eva@adventure.com', 'Eva@123', 'Faria Yesmin Farjana Eva', 'manager'),
            ('sumi_agent', 'sumi@adventure.com', 'Sumi@123', 'Sumi Akhter', 'agent'),
        ]
        for username, email, password, full_name, role in users:
            if not User.objects.filter(username=username).exists():
                name_parts = full_name.split(' ')
                u = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=name_parts[0], last_name=' '.join(name_parts[1:]),
                    role=role, is_staff=(role != 'customer'), is_superuser=(role == 'superadmin')
                )
                self.stdout.write(f'Created user: {username}')

        # Create 20 random customers
        for _ in range(20):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username, email=fake.email(), password='password123',
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    role='customer'
                )

        # 3. Destinations
        dest_data = [
            ('Cox’s Bazar', 'Chattogram', 'The world\'s longest natural sea beach.', 
             'Cox\'s Bazar is famous for its long sandy beach, world\'s longest natural sea beach. It is the top tourist destination in Bangladesh.'),
            ('Sajek Valley', 'Rangamati', 'The roof of Rangamati, surrounded by clouds.',
             'Sajek Valley is an emerging tourist spot in Bangladesh situated among the hills of the Kasalong range of mountains in Sajek union, Baghaichhari Upazila in Rangamati District.'),
            ('Bandarban', 'Bandarban', 'Home to the highest peaks of Bangladesh.',
             'Bandarban is a district in South-Eastern Bangladesh, and a part of the Chattogram Division. It is one of the three districts that make up the Chittagong Hill Tracts.'),
            ('Sylhet', 'Sylhet', 'The land of two leaves and a bud (tea gardens).',
             'Sylhet is a metropolitan city in northeastern Bangladesh. It is the administrative seat of Sylhet Division and is located on the bank of the Surma River.'),
            ('Saint Martin', 'Cox\'s Bazar', 'The only coral island in Bangladesh.',
             'Saint Martin\'s Island is a small island in the northeastern part of the Bay of Bengal, about 9 km south of the tip of the Cox\'s Bazar-Teknaf peninsula.'),
            ('Sundarbans', 'Khulna', 'The largest mangrove forest in the world.',
             'The Sundarbans is a mangrove area in the delta formed by the confluence of the Ganges, Brahmaputra and Meghna Rivers in the Bay of Bengal.'),
            ('Rangamati', 'Rangamati', 'The city of lakes and hills.',
             'Rangamati is the administrative headquarters of Rangamati Hill District in the Chittagong Hill Tracts of Bangladesh.'),
            ('Kuakata', 'Patuakhali', 'Where you can see both sunrise and sunset from the beach.',
             'Kuakata is a panoramic sea beach in southeastern Bangladesh. It is the only beach in South Asia where you can watch both the sunrise and sunset over the sea.'),
        ]
        dest_objs = []
        for title, dist, s_desc, full_desc in dest_data:
            dest, created = Destination.objects.get_or_create(title=title, defaults={
                'district': dist,
                'short_description': s_desc,
                'description': full_desc,
                'difficulty': random.choice(['easy', 'moderate', 'challenging']),
                'best_season': random.choice(['winter', 'summer', 'monsoon']),
                'min_budget': random.randint(3000, 8000),
                'max_budget': random.randint(10000, 25000),
                'is_featured': True,
                'weather_info': 'Pleasant weather during winter (Nov-Feb). Can be humid in summer.',
                'safety_tips': 'Always follow local guide instructions. Keep emergency contacts ready.',
            })
            dest_objs.append(dest)
            if created: self.stdout.write(f'Created destination: {title}')
        
        # Update existing destinations if they were already created with gibberish
        for title, dist, s_desc, full_desc in dest_data:
            Destination.objects.filter(title=title).update(description=full_desc, short_description=s_desc)

        # 4. Tour Categories
        cat_names = [('Couple Tour', 'fa-heart'), ('Family Tour', 'fa-users'), 
                     ('Honeymoon', 'fa-gem'), ('Adventure', 'fa-mountain'), 
                     ('Corporate', 'fa-briefcase'), ('Group Tour', 'fa-people-group')]
        cat_objs = []
        for name, icon in cat_names:
            cat, _ = TourCategory.objects.get_or_create(name=name, defaults={'icon': icon})
            cat_objs.append(cat)

        # 5. Tour Packages (approx 30)
        for i in range(30):
            dest = random.choice(dest_objs)
            cat = random.choice(cat_objs)
            title = f'{dest.title} {cat.name} Package {i+1}'
            price = random.randint(5000, 20000)
            TourPackage.objects.get_or_create(title=title, defaults={
                'category': cat,
                'destination': dest,
                'short_description': f'Exotic {cat.name} to {dest.title}.',
                'description': fake.text(max_nb_chars=1000),
                'duration_days': random.randint(2, 5),
                'duration_nights': random.randint(1, 4),
                'price': price,
                'discount_price': price - random.randint(500, 2000) if random.random() > 0.5 else None,
                'transport_type': random.choice(['bus', 'train', 'flight', 'boat']),
                'seats_total': random.randint(20, 50),
                'start_date': timezone.now().date() + timedelta(days=random.randint(10, 60)),
                'is_featured': random.random() > 0.7,
                'is_popular': random.random() > 0.6,
                'status': 'active',
                'included_services': 'Breakfast\nSightseeing\nLocal Guide\nTransport',
                'excluded_services': 'Personal Expenses\nTips\nLunch & Dinner',
            })

        # 6. Hotels & Rooms
        for dest in dest_objs:
            for i in range(3):
                hotel_name = f'{dest.title} {random.choice(["Resort", "Grand Hotel", "Palace", "Inn"])}'
                hotel, _ = Hotel.objects.get_or_create(name=hotel_name, defaults={
                    'destination': dest,
                    'short_description': f'Premium stay at {dest.title}.',
                    'description': fake.text(),
                    'address': f'{fake.street_address()}, {dest.title}',
                    'star_rating': random.randint(3, 5),
                    'is_featured': random.random() > 0.8,
                })
                # Add Rooms
                room_types = ['standard', 'deluxe', 'couple_suite', 'family_suite', 'executive_suite']
                for rt in room_types:
                    Room.objects.get_or_create(
                        hotel=hotel, 
                        room_number=str(random.randint(101, 505)), 
                        defaults={
                            'room_type': rt,
                            'price_per_night': random.randint(2000, 15000),
                            'capacity': random.randint(2, 4),
                            'has_ac': True,
                        }
                    )

        # 7. FAQs, Testimonials, Events
        for i in range(10):
            FAQ.objects.create(question=fake.sentence() + '?', answer=fake.paragraph())
            Testimonial.objects.create(name=fake.name(), designation=fake.job(), message=fake.paragraph(), rating=random.randint(4, 5), is_featured=True)
            Event.objects.create(
                title=f'Festival at {random.choice(dest_objs).title} {i+1}', 
                description=fake.text(), 
                location=fake.city(),
                start_date=timezone.now() + timedelta(days=random.randint(5, 30)),
                end_date=timezone.now() + timedelta(days=random.randint(31, 35)),
                price=random.randint(1000, 5000),
                is_featured=True
            )

        # 8. Blogs
        blog_cats = ['Travel Guide', 'Tips & Tricks', 'Stories', 'Food']
        for bc in blog_cats:
            cat, _ = BlogCategory.objects.get_or_create(name=bc)
            for i in range(5):
                BlogPost.objects.create(
                    title=f'Travel Story {bc} {i+1}: {fake.sentence()}',
                    category=cat,
                    author=User.objects.filter(role='superadmin').first(),
                    excerpt=fake.sentence(),
                    body=fake.text(max_nb_chars=2000),
                    status='published',
                    is_featured=random.random() > 0.7
                )

        # 9. Contact & Offices
        OfficeLocation.objects.get_or_create(country='Bangladesh', city='Dhaka', defaults={'address': 'Gulshan 2', 'is_headquarters': True, 'flag_emoji': '🇧🇩'})
        for country, city, flag in [('India', 'Kolkata', '🇮🇳'), ('USA', 'New York', '🇺🇸'), ('France', 'Paris', '🇫🇷')]:
            OfficeLocation.objects.get_or_create(country=country, city=city, defaults={'address': f'Travel St, {city}', 'flag_emoji': flag})

        for _ in range(15):
            ContactMessage.objects.create(name=fake.name(), email=fake.email(), subject=fake.sentence(), message=fake.paragraph())

        # 10. Random Bookings (approx 50)
        tours = list(TourPackage.objects.all())
        rooms = list(Room.objects.all())
        customers = list(User.objects.filter(role='customer'))
        for _ in range(50):
            u = random.choice(customers)
            b_type = random.choice(['tour', 'hotel'])
            status = random.choice(['pending', 'confirmed', 'completed'])
            p_status = 'paid' if status in ['confirmed', 'completed'] else 'due'
            
            if b_type == 'tour' and tours:
                t = random.choice(tours)
                Booking.objects.create(
                    user=u, booking_type='tour', tour_package=t,
                    check_in=t.start_date or timezone.now().date(),
                    check_out=t.end_date or (timezone.now().date() + timedelta(days=3)),
                    guest_name=u.get_full_name(), guest_email=u.email, guest_phone=fake.phone_number(),
                    total_price=t.effective_price, paid_amount=t.effective_price if p_status == 'paid' else 0,
                    status=status, payment_status=p_status
                )
            elif b_type == 'hotel' and rooms:
                r = random.choice(rooms)
                nights = random.randint(1, 4)
                total = r.price_per_night * nights
                Booking.objects.create(
                    user=u, booking_type='hotel', room=r,
                    check_in=timezone.now().date() - timedelta(days=random.randint(1, 10)),
                    check_out=timezone.now().date() + timedelta(days=random.randint(1, 5)),
                    guest_name=u.get_full_name(), guest_email=u.email, guest_phone=fake.phone_number(),
                    total_price=total, paid_amount=total if p_status == 'paid' else 0,
                    status=status, payment_status=p_status
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
