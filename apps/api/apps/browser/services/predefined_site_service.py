from apps.browser.models import PredefinedWebsite


def get_predefined_site(domain: str):
    return PredefinedWebsite.objects.filter(domain=domain).first()

