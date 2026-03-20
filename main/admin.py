from django.contrib import admin
from .models import Schedule, SchedulePage, Announcement, Material, ContactMessage

class SchedulePageInline(admin.TabularInline):
    model = SchedulePage
    extra = 2  # По умолчанию показываем 2 пустых формы для загрузки страниц
    fields = ['page_number', 'image']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_active', 'uploaded_at']
    list_filter = ['is_active', 'date']
    search_fields = ['title']
    inlines = [SchedulePageInline]  # Добавляем страницы прямо в форму расписания

@admin.register(SchedulePage)
class SchedulePageAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'page_number']
    list_filter = ['schedule']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_pinned', 'is_active']
    list_filter = ['is_pinned', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'content')
        }),
        ('Настройки', {
            'fields': ('is_pinned', 'is_active')
        }),
    )

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'uploaded_at']
    list_filter = ['subject', 'uploaded_at']
    search_fields = ['title', 'description', 'subject']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'message', 'created_at']
    
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанные"