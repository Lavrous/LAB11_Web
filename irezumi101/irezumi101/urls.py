# irezumi101/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from irezumi.views import page_not_found

admin.site.site_header = "Панель управления Irezumi 101"
admin.site.index_title = "База знаний японской татуировки"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('irezumi.urls')),
    path('masters/', include('masters.urls')),
    path('users/', include('users.urls', namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'irezumi.views.page_not_found'