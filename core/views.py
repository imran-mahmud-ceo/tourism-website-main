from django.shortcuts import render
from destinations.models import Destination
from tours.models import TourPackage, TourCategory
from blogs.models import BlogPost
from .models import SiteSettings, FAQ, Testimonial, Event, GalleryImage


def home(request):
    context = {
        'featured_destinations': Destination.objects.filter(is_featured=True, is_active=True)[:6],
        'popular_tours': TourPackage.objects.filter(is_popular=True, status='active')[:6],
        'featured_tours': TourPackage.objects.filter(is_featured=True, status='active')[:3],
        'tour_categories': TourCategory.objects.filter(is_active=True)[:8],
        'upcoming_events': Event.objects.filter(is_active=True, is_featured=True)[:5],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:6],
        'latest_blogs': BlogPost.objects.filter(status='published')[:3],
        'faqs': FAQ.objects.filter(is_active=True)[:8],
        'gallery_images': GalleryImage.objects.filter(is_featured=True)[:9],
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def privacy_policy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')
