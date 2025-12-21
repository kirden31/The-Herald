import django.conf
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
import django.urls

import herald.views

urlpatterns = [
    django.urls.path('', herald.views.HomeView.as_view()),
    django.urls.path('news/', django.urls.include('news.urls')),
    django.urls.path('admin/', admin.site.urls),
    django.urls.path('users/', django.urls.include('users.urls')),
    django.urls.path('users/', django.urls.include('django.contrib.auth.urls')),
] + i18n_patterns(django.urls.path('i18n/', django.urls.include('django.conf.urls.i18n')))

if django.conf.settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
