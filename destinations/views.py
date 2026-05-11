from django.shortcuts import render, get_object_or_404
from .models import Destination, DestinationReview
from tours.models import TourPackage
from hotels.models import Hotel


def destination_list(request):
    qs = Destination.objects.filter(is_active=True)
    q = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')
    season = request.GET.get('season', '')
    if q:
        qs = qs.filter(title__icontains=q)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)
    if season:
        qs = qs.filter(best_season=season)
    context = {
        'destinations': qs,
        'query': q,
        'difficulty': difficulty,
        'season': season,
        'difficulty_choices': Destination.DIFFICULTY,
        'season_choices': Destination.SEASON,
    }
    return render(request, 'destinations/list.html', context)


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    destination.view_count += 1
    destination.save(update_fields=['view_count'])
    context = {
        'destination': destination,
        'gallery': destination.gallery_images.all(),
        'reviews': destination.destination_reviews.select_related('author')[:10],
        'related_tours': TourPackage.objects.filter(destination=destination, status='active')[:4],
        'nearby_hotels': Hotel.objects.filter(destination=destination, is_active=True)[:4],
    }
    return render(request, 'destinations/detail.html', context)
