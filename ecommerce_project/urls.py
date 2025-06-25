from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('account/', include(('accounts.urls', 'account'), namespace='account')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

import os

if settings.DEBUG or os.environ.get('ENV') == 'production':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
