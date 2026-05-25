from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Subject, Topic, Note, HotTopic, Tag


def home(request):
    """Home page view"""
    subjects = Subject.objects.filter(is_active=True).annotate(
        notes_count=Count('topics__notes', filter=Q(topics__notes__is_published=True))
    )
    
    # Get recent notes
    recent_notes = Note.objects.filter(is_published=True).select_related(
        'topic', 'topic__subject'
    ).order_by('-created_at')[:6]
    
    # Get hot topics if available
    hot_topics = HotTopic.objects.filter(is_active=True).select_related('subject')[:5]
    
    context = {
        'subjects': subjects,
        'recent_notes': recent_notes,
        'hot_topics': hot_topics,
    }
    return render(request, 'notes/home.html', context)


def subject_detail(request, slug):
    """Subject detail page showing all topics"""
    subject = get_object_or_404(Subject, slug=slug, is_active=True)
    topics = subject.topics.filter(is_active=True).annotate(
        notes_count=Count('notes', filter=Q(notes__is_published=True))
    )
    
    context = {
        'subject': subject,
        'topics': topics,
    }
    return render(request, 'notes/subject_detail.html', context)


def topic_detail(request, subject_slug, topic_slug):
    """Topic detail page showing all notes"""
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)
    
    # Get filter parameters
    difficulty = request.GET.get('difficulty', '')
    importance = request.GET.get('importance', '')
    tag_slug = request.GET.get('tag', '')
    
    # Base queryset
    notes = topic.notes.filter(is_published=True).select_related('topic', 'topic__subject').prefetch_related('tags')
    
    # Apply filters
    if difficulty:
        notes = notes.filter(difficulty_level=difficulty)
    if importance:
        notes = notes.filter(importance_rating=importance)
    if tag_slug:
        notes = notes.filter(tags__slug=tag_slug)
    
    # Get all tags for this topic
    all_tags = Tag.objects.filter(notes__topic=topic, notes__is_published=True).distinct()
    
    # Pagination
    paginator = Paginator(notes, 12)  # 12 notes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'subject': subject,
        'topic': topic,
        'page_obj': page_obj,
        'all_tags': all_tags,
        'current_difficulty': difficulty,
        'current_importance': importance,
        'current_tag': tag_slug,
    }
    return render(request, 'notes/topic_detail.html', context)


def note_detail(request, subject_slug, topic_slug, note_slug):
    """Individual note detail page"""
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_active=True)
    note = get_object_or_404(Note, slug=note_slug, topic=topic, is_published=True)
    
    # Increment view count
    note.increment_views()
    
    # Get related notes (same topic, different note)
    related_notes = Note.objects.filter(
        topic=topic, 
        is_published=True
    ).exclude(id=note.id).order_by('-importance_rating')[:4]
    
    # Check if note is bookmarked
    bookmarks = request.session.get('bookmarks', [])
    is_bookmarked = note.id in bookmarks
    
    context = {
        'subject': subject,
        'topic': topic,
        'note': note,
        'related_notes': related_notes,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'notes/note_detail.html', context)


def search_notes(request):
    """Search functionality across all notes"""
    query = request.GET.get('q', '').strip()
    subject_filter = request.GET.get('subject', '')
    difficulty_filter = request.GET.get('difficulty', '')
    
    notes = Note.objects.filter(is_published=True).select_related(
        'topic', 'topic__subject'
    ).prefetch_related('tags')
    
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(key_points__icontains=query) |
            Q(exam_tips__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    if subject_filter:
        notes = notes.filter(topic__subject__slug=subject_filter)
    
    if difficulty_filter:
        notes = notes.filter(difficulty_level=difficulty_filter)
    
    # Pagination
    paginator = Paginator(notes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all subjects for filter
    subjects = Subject.objects.filter(is_active=True)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'subjects': subjects,
        'current_subject': subject_filter,
        'current_difficulty': difficulty_filter,
        'total_results': notes.count(),
    }
    return render(request, 'notes/search_results.html', context)


def toggle_bookmark(request, note_id):
    """Toggle bookmark for a note using session storage"""
    note = get_object_or_404(Note, id=note_id, is_published=True)
    
    # Get or create bookmarks list in session
    bookmarks = request.session.get('bookmarks', [])
    
    if note.id in bookmarks:
        bookmarks.remove(note.id)
        message = 'removed'
    else:
        bookmarks.append(note.id)
        message = 'added'
    
    request.session['bookmarks'] = bookmarks
    request.session.modified = True
    
    # Redirect back to the note or previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def bookmarks_list(request):
    """Display all bookmarked notes"""
    bookmark_ids = request.session.get('bookmarks', [])
    
    bookmarked_notes = Note.objects.filter(
        id__in=bookmark_ids,
        is_published=True
    ).select_related('topic', 'topic__subject').prefetch_related('tags')
    
    context = {
        'bookmarked_notes': bookmarked_notes,
    }
    return render(request, 'notes/bookmarks.html', context)


def hot_topics_list(request):
    """Display all hot topics (placeholder for future PYQ integration)"""
    subject_filter = request.GET.get('subject', '')
    
    hot_topics = HotTopic.objects.filter(is_active=True).select_related('subject').prefetch_related('related_notes')
    
    if subject_filter:
        hot_topics = hot_topics.filter(subject__slug=subject_filter)
    
    subjects = Subject.objects.filter(is_active=True)
    
    context = {
        'hot_topics': hot_topics,
        'subjects': subjects,
        'current_subject': subject_filter,
    }
    return render(request, 'notes/hot_topics.html', context)


def about(request):
    """About page"""
    return render(request, 'notes/about.html')


def how_to_use(request):
    """How to use page"""
    return render(request, 'notes/how_to_use.html')

# Made with Bob
