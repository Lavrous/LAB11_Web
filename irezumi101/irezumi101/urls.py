# irezumi101/urls.py
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Панель управления Irezumi 101"
admin.site.index_title = "База знаний японской татуировки"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('irezumi.urls')),
    path('masters/', include('masters.urls')), 
]

handler404 = 'irezumi.views.page_not_found'