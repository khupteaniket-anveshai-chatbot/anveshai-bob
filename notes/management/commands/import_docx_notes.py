"""
Generic Django management command to import notes from DOCX files.
Automatically parses structure and creates Subject, Topic, and Notes.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from notes.models import Subject, Topic, Tag, Note
import os
import sys

# Add utils directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from utils.docx_reader import read_docx_full, extract_sections


class Command(BaseCommand):
    help = 'Import notes from DOCX files in notes-source directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help='Name of the DOCX file in notes-source directory (e.g., "01. Cell.docx")'
        )
        parser.add_argument(
            '--subject',
            type=str,
            default='Science',
            help='Subject name (default: Science)'
        )
        parser.add_argument(
            '--topic',
            type=str,
            help='Topic name (if not provided, will use filename without extension)'
        )
        parser.add_argument(
            '--difficulty',
            type=str,
            default='medium',
            choices=['easy', 'medium', 'hard'],
            help='Default difficulty level for notes (default: medium)'
        )
        parser.add_argument(
            '--importance',
            type=int,
            default=3,
            choices=[1, 2, 3, 4, 5],
            help='Default importance rating (1-5, default: 3)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        subject_name = options['subject']
        topic_name = options['topic']
        difficulty = options['difficulty']
        importance = options['importance']
        dry_run = options['dry_run']

        # Construct file path
        file_path = os.path.join('notes-source', filename)
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(self.style.WARNING(f'Reading file: {file_path}'))

        # If topic name not provided, use filename without extension
        if not topic_name:
            topic_name = os.path.splitext(filename)[0]
            # Remove numbering like "01. " from the beginning
            if '. ' in topic_name:
                topic_name = topic_name.split('. ', 1)[1]

        self.stdout.write(f'Subject: {subject_name}')
        self.stdout.write(f'Topic: {topic_name}')
        self.stdout.write('')

        # Read the DOCX file
        try:
            sections = extract_sections(file_path)
            self.stdout.write(self.style.SUCCESS(f'Found {len(sections)} sections in document'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file: {str(e)}'))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING('\n=== DRY RUN MODE - No data will be saved ===\n'))
            self._display_sections(sections)
            return

        # Create or get Subject
        subject, created = Subject.objects.get_or_create(
            name=subject_name,
            defaults={
                'description': f'{subject_name} notes for competitive exams',
                'icon': 'fas fa-book',
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created subject: {subject.name}'))
        else:
            self.stdout.write(f'✓ Using existing subject: {subject.name}')

        # Create or get Topic
        topic, created = Topic.objects.get_or_create(
            subject=subject,
            title=topic_name,
            defaults={
                'description': f'Comprehensive notes on {topic_name}',
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created topic: {topic.title}'))
        else:
            self.stdout.write(f'✓ Using existing topic: {topic.title}')

        # Create default tags
        important_tag, _ = Tag.objects.get_or_create(
            name='Important',
            defaults={'color': '#dc3545'}
        )
        basic_tag, _ = Tag.objects.get_or_create(
            name='Basic Concept',
            defaults={'color': '#28a745'}
        )

        # Import sections as notes
        notes_created = 0
        notes_updated = 0
        
        for section_title, section_content in sections.items():
            if not section_content:
                continue

            # Convert content list to HTML
            content_html = self._format_content_as_html(section_content)
            
            # Extract key points (first few lines or bullet points)
            key_points = self._extract_key_points(section_content)
            
            # Calculate estimated read time (rough estimate: 200 words per minute)
            word_count = sum(len(line.split()) for line in section_content)
            read_time = max(1, word_count // 200)

            # Create or update note
            note, created = Note.objects.update_or_create(
                topic=topic,
                title=section_title,
                defaults={
                    'content': content_html,
                    'key_points': key_points,
                    'difficulty_level': difficulty,
                    'importance_rating': importance,
                    'estimated_read_time': read_time,
                    'is_published': True
                }
            )

            # Add tags
            note.tags.add(important_tag)
            if 'definition' in section_title.lower() or 'basic' in section_title.lower():
                note.tags.add(basic_tag)

            if created:
                notes_created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created note: {section_title}'))
            else:
                notes_updated += 1
                self.stdout.write(f'  ✓ Updated note: {section_title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Import completed!'))
        self.stdout.write(self.style.SUCCESS(f'Notes created: {notes_created}'))
        self.stdout.write(self.style.SUCCESS(f'Notes updated: {notes_updated}'))
        self.stdout.write(self.style.SUCCESS(f'Total sections: {len(sections)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def _format_content_as_html(self, content_lines):
        """Convert content lines to HTML format"""
        html_parts = []
        current_list = []
        
        for line in content_lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's a bullet point
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                current_list.append(line.lstrip('•-* '))
            else:
                # If we have accumulated list items, close the list
                if current_list:
                    html_parts.append('<ul>')
                    for item in current_list:
                        html_parts.append(f'<li>{item}</li>')
                    html_parts.append('</ul>')
                    current_list = []
                
                # Check if it's a heading (short line, possibly ends with :)
                if len(line) < 100 and (line.endswith(':') or line.isupper()):
                    html_parts.append(f'<h4>{line}</h4>')
                else:
                    html_parts.append(f'<p>{line}</p>')
        
        # Close any remaining list
        if current_list:
            html_parts.append('<ul>')
            for item in current_list:
                html_parts.append(f'<li>{item}</li>')
            html_parts.append('</ul>')
        
        return '\n'.join(html_parts)

    def _extract_key_points(self, content_lines):
        """Extract key points from content"""
        key_points = []
        for line in content_lines[:10]:  # Take first 10 lines
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                key_points.append(line)
            elif line and len(line) < 150:  # Short, important lines
                key_points.append(f'• {line}')
        
        return '\n'.join(key_points[:8])  # Limit to 8 key points

    def _display_sections(self, sections):
        """Display sections for dry run"""
        for i, (section_title, section_content) in enumerate(sections.items(), 1):
            self.stdout.write(f'\n{i}. {section_title}')
            self.stdout.write('-' * 60)
            content_preview = '\n'.join(section_content[:5])
            self.stdout.write(content_preview)
            if len(section_content) > 5:
                self.stdout.write(f'... ({len(section_content) - 5} more lines)')

# Made with Bob
