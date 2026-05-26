"""
Views for handling notes import workflow via web interface.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import NotesImportSession, Subject, Topic, Note, Tag
import json
import re


@staff_member_required
def import_notes_form(request):
    """Display form to paste raw notes"""
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        topic_name = request.POST.get('topic_name')
        raw_notes = request.POST.get('raw_notes')
        
        if not all([subject_name, topic_name, raw_notes]):
            messages.error(request, 'All fields are required!')
            return render(request, 'notes/import_form.html')
        
        # Create import session
        session = NotesImportSession.objects.create(
            subject_name=subject_name,
            topic_name=topic_name,
            raw_notes=raw_notes,
            status='pending'
        )
        
        # Format notes
        formatted_notes = format_raw_notes(raw_notes)
        session.formatted_notes = formatted_notes
        session.notes_count = len(formatted_notes)
        session.save()
        
        messages.success(request, f'Notes formatted! Found {len(formatted_notes)} notes. Please review.')
        return redirect('notes:import_review', session_id=session.id)
    
    return render(request, 'notes/import_form.html')


@staff_member_required
def import_review(request, session_id):
    """Review and edit formatted notes before importing"""
    session = get_object_or_404(NotesImportSession, id=session_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            # Import notes to database
            try:
                import_notes_to_db(session)
                session.status = 'imported'
                session.imported_at = timezone.now()
                session.save()
                messages.success(request, f'Successfully imported {session.notes_count} notes!')
                return redirect('admin:notes_notesimportsession_changelist')
            except Exception as e:
                messages.error(request, f'Error importing notes: {str(e)}')
        
        elif action == 'reject':
            session.status = 'rejected'
            session.save()
            messages.warning(request, 'Import session rejected.')
            return redirect('admin:notes_notesimportsession_changelist')
        
        elif action == 'edit':
            # Update formatted notes from form
            updated_notes = []
            for i, note in enumerate(session.formatted_notes):
                updated_note = {
                    'title': request.POST.get(f'title_{i}', note['title']),
                    'content': request.POST.get(f'content_{i}', note['content']),
                    'key_points': request.POST.get(f'key_points_{i}', note['key_points']),
                    'difficulty_level': request.POST.get(f'difficulty_{i}', note['difficulty_level']),
                    'importance_rating': int(request.POST.get(f'importance_{i}', note['importance_rating'])),
                }
                updated_notes.append(updated_note)
            
            session.formatted_notes = updated_notes
            session.save()
            messages.success(request, 'Notes updated successfully!')
    
    context = {
        'session': session,
        'formatted_notes': session.formatted_notes,
    }
    return render(request, 'notes/import_review.html', context)


@staff_member_required
def import_sessions_list(request):
    """List all import sessions"""
    sessions = NotesImportSession.objects.all()
    context = {
        'sessions': sessions,
    }
    return render(request, 'notes/import_sessions_list.html', context)


def format_raw_notes(raw_text):
    """
    Parse raw notes text and format into structured data.
    Returns list of note dictionaries.
    """
    notes = []
    lines = raw_text.strip().split('\n')
    current_note = None
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a main heading (short line, no ending punctuation except :)
        if is_heading(line):
            # Save previous note
            if current_note and current_note.get('title'):
                notes.append(current_note)
            
            # Start new note
            current_note = {
                'title': line.rstrip(':'),
                'content': [],
                'key_points': [],
                'extra_info': [],
                'difficulty_level': 'medium',
                'importance_rating': 3,
            }
            current_section = 'content'
        
        elif current_note:
            # Check for special sections
            if line.lower().startswith('extra'):
                current_section = 'extra_info'
                continue
            elif line.lower().startswith('key points'):
                current_section = 'key_points'
                continue
            
            # Add content to appropriate section
            if current_section == 'content':
                current_note['content'].append(line)
            elif current_section == 'key_points':
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    current_note['key_points'].append(line.lstrip('•-* '))
                else:
                    current_note['key_points'].append(line)
            elif current_section == 'extra_info':
                current_note['extra_info'].append(line)
    
    # Save last note
    if current_note and current_note.get('title'):
        notes.append(current_note)
    
    # Format notes for display
    formatted_notes = []
    for note in notes:
        formatted_note = {
            'title': note['title'],
            'content': format_content_html(note['content']),
            'key_points': '\n'.join(f"• {point}" for point in note['key_points']),
            'extra_info': format_content_html(note['extra_info']) if note['extra_info'] else '',
            'difficulty_level': note['difficulty_level'],
            'importance_rating': note['importance_rating'],
        }
        formatted_notes.append(formatted_note)
    
    return formatted_notes


def is_heading(line):
    """Determine if a line is a heading"""
    # Headings are usually:
    # - Short (< 100 chars)
    # - Don't end with . , ;
    # - May end with :
    if len(line) > 100:
        return False
    
    if line.endswith('.') or line.endswith(',') or line.endswith(';'):
        return False
    
    word_count = len(line.split())
    if word_count <= 8:
        return True
    
    return False


def format_content_html(content_lines):
    """Convert content lines to HTML"""
    if not content_lines:
        return ''
    
    html_parts = []
    in_list = False
    
    for line in content_lines:
        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f'<li>{line.lstrip("•-* ")}</li>')
        else:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            
            if line.endswith(':'):
                html_parts.append(f'<h4>{line}</h4>')
            else:
                html_parts.append(f'<p>{line}</p>')
    
    if in_list:
        html_parts.append('</ul>')
    
    return '\n'.join(html_parts)


def import_notes_to_db(session):
    """Import formatted notes from session to database"""
    # Get or create Subject
    subject, _ = Subject.objects.get_or_create(
        name=session.subject_name,
        defaults={
            'description': f'{session.subject_name} notes for competitive exams',
            'icon': 'fas fa-book',
            'order': 1
        }
    )
    
    # Get or create Topic
    topic, _ = Topic.objects.get_or_create(
        subject=subject,
        title=session.topic_name,
        defaults={
            'description': f'Comprehensive notes on {session.topic_name}',
            'order': 1
        }
    )
    
    # Get tags
    important_tag, _ = Tag.objects.get_or_create(
        name='Important',
        defaults={'color': '#dc3545'}
    )
    basic_tag, _ = Tag.objects.get_or_create(
        name='Basic Concept',
        defaults={'color': '#28a745'}
    )
    exam_tag, _ = Tag.objects.get_or_create(
        name='Frequently Asked',
        defaults={'color': '#ffc107'}
    )
    
    # Import each note
    for note_data in session.formatted_notes:
        # Combine content and extra info
        full_content = note_data['content']
        if note_data.get('extra_info'):
            full_content += f'\n<h4>Extra Information:</h4>\n{note_data["extra_info"]}'
        
        # Calculate read time
        content_length = len(full_content)
        read_time = max(1, content_length // 500)
        
        # Create or update note
        note, created = Note.objects.update_or_create(
            topic=topic,
            title=note_data['title'],
            defaults={
                'content': full_content,
                'key_points': note_data['key_points'],
                'difficulty_level': note_data['difficulty_level'],
                'importance_rating': note_data['importance_rating'],
                'estimated_read_time': read_time,
                'is_published': True
            }
        )
        
        # Add tags
        tags = [important_tag]
        if note_data['difficulty_level'] == 'easy':
            tags.append(basic_tag)
        if note_data['importance_rating'] >= 4:
            tags.append(exam_tag)
        
        note.tags.set(tags)

# Made with Bob
