from django.contrib import admin
from .models import Subject, Topic, Tag, Note, HotTopic


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order', 'get_topics_count', 'get_notes_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'is_active', 'order', 'get_notes_count', 'created_at']
    list_filter = ['subject', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'subject__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'order']
    ordering = ['subject', 'order', 'title']
    autocomplete_fields = ['subject']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'topic', 
        'difficulty_level', 
        'importance_rating', 
        'is_published', 
        'views_count',
        'estimated_read_time',
        'updated_at'
    ]
    list_filter = [
        'topic__subject',
        'topic',
        'difficulty_level', 
        'importance_rating', 
        'is_published',
        'tags',
        'created_at'
    ]
    search_fields = ['title', 'content', 'key_points', 'exam_tips', 'topic__title']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'difficulty_level', 'importance_rating']
    filter_horizontal = ['tags']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'title', 'slug', 'tags')
        }),
        ('Content', {
            'fields': ('content', 'key_points', 'exam_tips', 'common_mistakes')
        }),
        ('Metadata', {
            'fields': ('difficulty_level', 'importance_rating', 'estimated_read_time')
        }),
        ('Status', {
            'fields': ('is_published', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-importance_rating', 'topic', 'title']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('topic', 'topic__subject').prefetch_related('tags')


@admin.register(HotTopic)
class HotTopicAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'subject', 
        'frequency', 
        'last_appeared_year', 
        'is_active',
        'created_at'
    ]
    list_filter = ['subject', 'is_active', 'last_appeared_year']
    search_fields = ['title', 'description', 'subject__name']
    filter_horizontal = ['related_notes']
    list_editable = ['is_active', 'frequency']
    ordering = ['-frequency', '-last_appeared_year']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('subject', 'title', 'description')
        }),
        ('PYQ Analysis', {
            'fields': ('frequency', 'last_appeared_year')
        }),
        ('Related Content', {
            'fields': ('related_notes',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


# Customize admin site header and title
admin.site.site_header = "AnveshAI Admin"
admin.site.site_title = "AnveshAI Admin Portal"
admin.site.index_title = "Welcome to AnveshAI Administration"

# Made with Bob
