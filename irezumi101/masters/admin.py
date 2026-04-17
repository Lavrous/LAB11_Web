from django.contrib import admin
from .models import Master, Studio
# Register your models here.
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'century', 'studio')
    list_display_links = ('id', 'name')
    list_editable = ('century',)
    search_fields = ['name', 'bio']
    list_filter = ['century']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    list_display_links = ('name',)
