"""
Django management command to import notes from markdown review files.
Reads the .md file, parses it, and imports to database.
"""

from django.core.management.base import BaseCommand
from notes.models import Subject, Topic, Tag, Note
import re
import os


class Command(BaseCommand):
    help = 'Import notes from markdown review file'

    def add_arguments(self, parser):
        parser.add_argument(
            'markdown_file',
            type=str,
            help='Path to markdown file (e.g., notes-formatted/cell_biology_part1_review.md)'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing notes for this topic before importing'
        )
        parser.add_argument(
            '--delete-after',
            action='store_true',
            help='Delete markdown file after successful import'
        )

    def handle(self, *args, **options):
        markdown_file = options['markdown_file']
        clear_existing = options['clear_existing']
        delete_after = options['delete_after']
        
        if not os.path.exists(markdown_file):
            self.stdout.write(self.style.ERROR(f'File not found: {markdown_file}'))
            return
        
        self.stdout.write(f'Reading file: {markdown_file}\n')
        
        # Parse markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract subject and topic from header
        subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
        topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', content)
        
        if not subject_match or not topic_match:
            self.stdout.write(self.style.ERROR('Could not find Subject or Topic in markdown file'))
            return
        
        subject_name = subject_match.group(1).strip()
        topic_name = topic_match.group(1).strip()
        
        self.stdout.write(f'Subject: {subject_name}')
        self.stdout.write(f'Topic: {topic_name}\n')
        
        # Get or create Subject
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

        # Get or create Topic
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

        # Clear existing notes if requested
        if clear_existing:
            deleted_count = Note.objects.filter(topic=topic).delete()[0]
            self.stdout.write(self.style.WARNING(f'✓ Deleted {deleted_count} existing notes\n'))

        # Create tags
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
        
        # Parse notes from markdown
        notes_data = self.parse_notes_from_markdown(content)
        
        # Import notes
        notes_created = 0
        notes_updated = 0

        for note_data in notes_data:
            # Determine tags based on importance and difficulty
            tags = [important_tag]
            if note_data['difficulty_level'] == 'easy':
                tags.append(basic_tag)
            if note_data['importance_rating'] >= 4:
                tags.append(exam_tag)
            
            note, created = Note.objects.update_or_create(
                topic=topic,
                title=note_data['title'],
                defaults={
                    'content': note_data['content'],
                    'key_points': note_data['key_points'],
                    'exam_tips': note_data.get('exam_tips', ''),
                    'difficulty_level': note_data['difficulty_level'],
                    'importance_rating': note_data['importance_rating'],
                    'estimated_read_time': note_data['estimated_read_time'],
                    'is_published': True
                }
            )

            # Add tags
            note.tags.set(tags)

            if created:
                notes_created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {note.title}'))
            else:
                notes_updated += 1
                self.stdout.write(f'  ✓ Updated: {note.title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Import completed!'))
        self.stdout.write(self.style.SUCCESS(f'Notes created: {notes_created}'))
        self.stdout.write(self.style.SUCCESS(f'Notes updated: {notes_updated}'))
        self.stdout.write(self.style.SUCCESS(f'Total notes: {len(notes_data)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Delete markdown file if requested
        if delete_after:
            os.remove(markdown_file)
            self.stdout.write(self.style.WARNING(f'\n✓ Deleted file: {markdown_file}'))
    
    def parse_notes_from_markdown(self, content):
        """Parse notes from markdown content"""
        notes = []
        
        # Split by note sections (## followed by number)
        note_sections = re.split(r'\n## \d+\.\s+', content)[1:]  # Skip header
        
        for section in note_sections:
            note_data = {}
            
            # Extract title
            title_match = re.search(r'\*\*Title:\*\*\s*(.+)', section)
            if title_match:
                note_data['title'] = title_match.group(1).strip()
            
            # Extract content
            content_match = re.search(r'\*\*Content:\*\*\s*\n(.*?)\n\*\*', section, re.DOTALL)
            if content_match:
                note_data['content'] = self.convert_markdown_to_html(content_match.group(1).strip())
            
            # Extract key points
            key_points_match = re.search(r'\*\*Key Points:\*\*\s*\n(.*?)\n\*\*', section, re.DOTALL)
            if key_points_match:
                note_data['key_points'] = key_points_match.group(1).strip()
            
            # Extract exam tips if present
            exam_tips_match = re.search(r'\*\*Extra Information:\*\*\s*\n(.*?)(?:\n\*\*|$)', section, re.DOTALL)
            if exam_tips_match:
                note_data['exam_tips'] = self.convert_markdown_to_html(exam_tips_match.group(1).strip())
            else:
                note_data['exam_tips'] = ''
            
            # Extract difficulty
            difficulty_match = re.search(r'\*\*Difficulty:\*\*\s*(\w+)', section)
            if difficulty_match:
                note_data['difficulty_level'] = difficulty_match.group(1).lower()
            else:
                note_data['difficulty_level'] = 'medium'
            
            # Extract importance (count stars)
            importance_match = re.search(r'\*\*Importance:\*\*\s*⭐+\s*\((\d+)/5\)', section)
            if importance_match:
                note_data['importance_rating'] = int(importance_match.group(1))
            else:
                note_data['importance_rating'] = 3
            
            # Estimate read time based on content length
            content_length = len(note_data.get('content', ''))
            note_data['estimated_read_time'] = max(1, content_length // 500)
            
            if note_data.get('title'):
                notes.append(note_data)
        
        return notes
    
    def convert_markdown_to_html(self, text):
        """Convert simple markdown to HTML including tables"""
        lines = text.split('\n')
        html_lines = []
        in_table = False
        table_rows = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this is a table line (contains |)
            if '|' in line and line.count('|') >= 2:
                if not in_table:
                    in_table = True
                    table_rows = []
                
                # Skip separator line (|---|---|)
                if re.match(r'^\|[\s\-|]+\|$', line):
                    i += 1
                    continue
                
                # Parse table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last
                table_rows.append(cells)
                i += 1
                
                # Check if next line is still part of table
                if i < len(lines) and '|' not in lines[i]:
                    # End of table, convert to HTML
                    html_lines.append(self.convert_table_to_html(table_rows))
                    in_table = False
                    table_rows = []
                elif i >= len(lines):
                    # End of content, convert table
                    html_lines.append(self.convert_table_to_html(table_rows))
                    in_table = False
                continue
            
            # If we were in a table but this line isn't, close the table
            if in_table:
                html_lines.append(self.convert_table_to_html(table_rows))
                in_table = False
                table_rows = []
            
            # Convert bullet points
            if line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.startswith('• '):
                html_lines.append(f'<li>{line[2:]}</li>')
            # Convert bold
            elif '**' in line:
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                html_lines.append(f'<p>{line}</p>')
            # Regular paragraph
            elif line:
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('')
            
            i += 1
        
        # Close any remaining table
        if in_table:
            html_lines.append(self.convert_table_to_html(table_rows))
        
        # Wrap consecutive <li> tags in <ul>
        result = '\n'.join(html_lines)
        result = re.sub(r'(<li>.*?</li>\s*)+', lambda m: f'<ul>\n{m.group(0)}\n</ul>', result, flags=re.DOTALL)
        
        return result
    
    def convert_table_to_html(self, rows):
        """Convert table rows to HTML table"""
        if not rows:
            return ''
        
        html = ['<table border="1" style="border-collapse: collapse; width: 100%;">']
        
        # First row is header
        if rows:
            html.append('<thead><tr>')
            for cell in rows[0]:
                html.append(f'<th style="padding: 8px; background-color: #f2f2f2;">{cell}</th>')
            html.append('</tr></thead>')
        
        # Remaining rows are body
        if len(rows) > 1:
            html.append('<tbody>')
            for row in rows[1:]:
                html.append('<tr>')
                for cell in row:
                    html.append(f'<td style="padding: 8px; border: 1px solid #ddd;">{cell}</td>')
                html.append('</tr>')
            html.append('</tbody>')
        
        html.append('</table>')
        return '\n'.join(html)

# Made with Bob
