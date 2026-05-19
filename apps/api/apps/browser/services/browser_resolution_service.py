from urllib.parse import urlparse

from apps.browser.models import Domain, PredefinedWebsite
from apps.browser.services.domain_service import normalize_domain


def normalize_url(value: str) -> tuple[str, str]:
    value = value.strip()
    if "://" not in value:
        value = f"https://{value}"
    parsed = urlparse(value)
    domain = normalize_domain(parsed.netloc or parsed.path)
    scheme = parsed.scheme if parsed.scheme in {"http", "https"} else "https"
    return f"{scheme}://www.{domain}", domain


def resolve_url(value: str):
    normalized_url, domain_name = normalize_url(value)
    predefined = PredefinedWebsite.objects.filter(domain=domain_name).first()
    if predefined:
        return {
            "url": normalized_url,
            "site_type": "predefined",
            "trust_level": predefined.trust_level,
            "html": predefined.html,
            "css": predefined.css,
            "js": predefined.js,
            "sandbox_policy": {"sandbox": False, "external_fetch": False},
            "content_version": 1,
            "owner": None,
            "allowed_game_capabilities": [predefined.behavior_key],
        }
    domain = Domain.objects.filter(name=domain_name, status="active").select_related("website").first()
    if domain and hasattr(domain, "website"):
        site = domain.website
        return {
            "url": normalized_url,
            "site_type": site.site_type,
            "trust_level": site.trust_level,
            "html": site.html,
            "css": site.css,
            "js": site.js,
            "sandbox_policy": site.sandbox_policy,
            "content_version": site.content_version,
            "owner": str(site.owner_id) if site.owner_id else None,
            "allowed_game_capabilities": [],
        }
    return None

