from django.contrib import admin
from django.contrib import messages
from .models import Motif, Category, TagPost

class HasImageFilter(admin.SimpleListFilter):
    title = 'Наличие изображения'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'С картинкой'),
            ('no', 'Без картинки'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image__exact='')
        if self.value() == 'no':
            return queryset.filter(image__exact='')
        return queryset

@admin.register(Motif)
class MotifAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'is_published', 'time_create', 'brief_info', 'image_status')
    list_display_links = ('id', 'title')
    list_editable = ('cat', ) # Редактирование прямо в списке
    ordering = ['-time_create', 'title'] # Сортировка
    list_per_page = 10

    search_fields = ['title', 'cat__name']
    list_filter = ['cat', HasImageFilter, 'is_published']

    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']
    readonly_fields = ['time_create', 'time_update', 'views_count']

    @admin.display(description="Объем текста", ordering='content')
    def brief_info(self, obj):
        return f"{len(obj.content)} символов"

    @admin.display(description="Иллюстрация")
    def image_status(self, obj):
        if obj.image:
            return "✅ Загружена"
        return "❌ Отсутствует"

    @admin.action(description="Опубликовать выбранные мотивы")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Motif.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей: теперь они на сайте.", messages.SUCCESS)

    @admin.action(description="Снять с публикации (в черновик)")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Motif.Status.DRAFT)
        self.message_user(request, f"Внимание! {count} записей скрыто с сайта.", messages.WARNING)

    # Регистрируем действия
    actions = ['set_published', 'set_draft']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    prepopulated_fields = {"slug": ("tag",)}
