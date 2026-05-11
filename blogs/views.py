from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory


def blog_list(request):
    qs = BlogPost.objects.filter(status='published').select_related('author', 'category')
    category_slug = request.GET.get('category', '')
    q = request.GET.get('q', '')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'blogs/list.html', {
        'posts': qs,
        'categories': BlogCategory.objects.all(),
        'selected_category': category_slug,
        'query': q,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    post.view_count += 1
    post.save(update_fields=['view_count'])
    related = BlogPost.objects.filter(
        category=post.category, status='published'
    ).exclude(pk=post.pk)[:3]
    return render(request, 'blogs/detail.html', {'post': post, 'related': related})
