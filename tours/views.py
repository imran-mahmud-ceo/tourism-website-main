from django.shortcuts import render, get_object_or_404
from .models import TourPackage, TourCategory


def tour_list(request):
    qs = TourPackage.objects.filter(status='active').select_related('category', 'destination')
    q = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    duration = request.GET.get('duration', '')

    if q:
        qs = qs.filter(title__icontains=q)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)
    if duration:
        qs = qs.filter(duration_days__lte=int(duration))

    context = {
        'tours': qs,
        'categories': TourCategory.objects.filter(is_active=True),
        'query': q,
        'selected_category': category_slug,
    }
    return render(request, 'tours/list.html', context)


def tour_detail(request, slug):
    tour = get_object_or_404(TourPackage, slug=slug, status='active')
    tour.view_count += 1
    tour.save(update_fields=['view_count'])
    related = TourPackage.objects.filter(
        category=tour.category, status='active'
    ).exclude(pk=tour.pk)[:3]
    context = {
        'tour': tour,
        'gallery': tour.gallery_images.all(),
        'itinerary': tour.itinerary.all(),
        'reviews': tour.tour_reviews.select_related('author')[:8],
        'related_tours': related,
    }
    return render(request, 'tours/detail.html', context)
