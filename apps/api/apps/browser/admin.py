from django.contrib import admin

from .models import Certificate, Domain, PredefinedWebsite, SearchIndexEntry, Website, WebsiteDeployment, WebsiteFile


admin.site.register(Domain)
admin.site.register(Certificate)
admin.site.register(Website)
admin.site.register(WebsiteFile)
admin.site.register(WebsiteDeployment)
admin.site.register(PredefinedWebsite)
admin.site.register(SearchIndexEntry)

