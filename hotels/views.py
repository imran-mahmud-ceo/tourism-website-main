from django.shortcuts import render, get_object_or_404
from .models import Hotel


def hotel_list(request):
    qs = Hotel.objects.filter(is_active=True).select_related('destination')
    q = request.GET.get('q', '')
    stars = request.GET.get('stars', '')
    if q:
        qs = qs.filter(name__icontains=q)
    if stars:
        qs = qs.filter(star_rating=stars)
    return render(request, 'hotels/list.html', {'hotels': qs, 'query': q, 'stars': stars})


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug, is_active=True)
    context = {
        'hotel': hotel,
        'gallery': hotel.gallery_images.all(),
        'rooms': hotel.rooms.filter(is_available=True),
    }
    return render(request, 'hotels/detail.html', context)
