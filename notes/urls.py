from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Subject and Topic views
    path('subject/<slug:slug>/', views.subject_detail, name='subject_detail'),
    path('subject/<slug:subject_slug>/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    
    # Note detail
    path('subject/<slug:subject_slug>/<slug:topic_slug>/<slug:note_slug>/', views.note_detail, name='note_detail'),
    
    # Search
    path('search/', views.search_notes, name='search'),
    
    # Bookmarks
    path('bookmarks/', views.bookmarks_list, name='bookmarks'),
    path('bookmark/toggle/<int:note_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    
    # Hot Topics
    path('hot-topics/', views.hot_topics_list, name='hot_topics'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('how-to-use/', views.how_to_use, name='how_to_use'),
]

# Made with Bob
