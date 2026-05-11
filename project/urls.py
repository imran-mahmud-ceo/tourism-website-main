from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('destinations/', include('destinations.urls', namespace='destinations')),
    path('tours/', include('tours.urls', namespace='tours')),
    path('hotels/', include('hotels.urls', namespace='hotels')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('blog/', include('blogs.urls', namespace='blogs')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('', include('core.urls', namespace='core')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)