from .models import SiteSettings


def site_context(request):
    """Inject global site settings into every template."""
    settings = SiteSettings.get_settings()
    return {'site': settings}
