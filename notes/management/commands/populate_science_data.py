from django.core.management.base import BaseCommand
from notes.models import Subject, Topic, Tag, Note


class Command(BaseCommand):
    help = 'Populate database with sample Science subject data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating Science data...')

        # Create Science subject
        science, created = Subject.objects.get_or_create(
            name='Science',
            defaults={
                'description': 'General Science for MPSC exams covering Physics, Chemistry, and Biology',
                'icon': 'fas fa-flask',
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created subject: {science.name}'))

        # Create Tags
        tags_data = [
            ('Important', '#dc3545'),
            ('Frequently Asked', '#ffc107'),
            ('Basic Concept', '#28a745'),
            ('Advanced', '#6f42c1'),
            ('Formula', '#17a2b8'),
        ]
        tags = {}
        for tag_name, color in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'color': color}
            )
            tags[tag_name] = tag
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))

        # Create Physics Topic
        physics, created = Topic.objects.get_or_create(
            subject=science,
            title='Physics',
            defaults={
                'description': 'Fundamental concepts of Physics including mechanics, thermodynamics, and optics',
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created topic: {physics.title}'))

        # Create sample Physics notes
        physics_notes = [
            {
                'title': "Newton's Laws of Motion",
                'content': '''<h3>Newton's Three Laws of Motion</h3>
<p><strong>First Law (Law of Inertia):</strong> An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an external force.</p>
<p><strong>Second Law:</strong> The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. Formula: F = ma</p>
<p><strong>Third Law:</strong> For every action, there is an equal and opposite reaction.</p>
<h4>Applications:</h4>
<ul>
<li>Rocket propulsion</li>
<li>Walking and running</li>
<li>Vehicle motion</li>
</ul>''',
                'key_points': '''• First Law: Inertia - objects resist changes in motion
• Second Law: F = ma (Force = mass × acceleration)
• Third Law: Action-Reaction pairs
• All three laws work together to explain motion
• Important for understanding mechanics''',
                'exam_tips': '''<p><strong>Common Questions:</strong></p>
<ul>
<li>Numerical problems on F = ma</li>
<li>Real-life examples of each law</li>
<li>Relationship between force, mass, and acceleration</li>
</ul>
<p><strong>Tips:</strong> Remember the formula F = ma and practice numerical problems.</p>''',
                'common_mistakes': '''• Confusing mass with weight
• Not considering all forces in F = ma
• Forgetting that action-reaction pairs act on different objects
• Mixing up the three laws''',
                'difficulty_level': 'medium',
                'importance_rating': 5,
                'estimated_read_time': 8,
                'tags': ['Important', 'Formula', 'Frequently Asked']
            },
            {
                'title': 'Work, Energy and Power',
                'content': '''<h3>Work, Energy and Power</h3>
<p><strong>Work:</strong> Work is done when a force causes displacement. W = F × d × cos(θ)</p>
<p><strong>Energy:</strong> The capacity to do work. Types include:</p>
<ul>
<li>Kinetic Energy: KE = ½mv²</li>
<li>Potential Energy: PE = mgh</li>
</ul>
<p><strong>Power:</strong> Rate of doing work. P = W/t</p>
<h4>Law of Conservation of Energy:</h4>
<p>Energy can neither be created nor destroyed, only converted from one form to another.</p>''',
                'key_points': '''• Work = Force × Displacement × cos(angle)
• Kinetic Energy = ½mv²
• Potential Energy = mgh
• Power = Work/Time
• Energy is conserved in all processes''',
                'exam_tips': '''<p><strong>Focus Areas:</strong></p>
<ul>
<li>Formula-based numerical problems</li>
<li>Unit conversions (Joule, Watt)</li>
<li>Energy conservation examples</li>
</ul>''',
                'common_mistakes': '''• Forgetting to consider the angle in work formula
• Confusing energy with power
• Not applying conservation of energy correctly''',
                'difficulty_level': 'medium',
                'importance_rating': 4,
                'estimated_read_time': 7,
                'tags': ['Important', 'Formula']
            }
        ]

        for note_data in physics_notes:
            tag_names = note_data.pop('tags', [])
            note, created = Note.objects.get_or_create(
                topic=physics,
                title=note_data['title'],
                defaults=note_data
            )
            if created:
                for tag_name in tag_names:
                    if tag_name in tags:
                        note.tags.add(tags[tag_name])
                self.stdout.write(self.style.SUCCESS(f'Created note: {note.title}'))

        # Create Chemistry Topic
        chemistry, created = Topic.objects.get_or_create(
            subject=science,
            title='Chemistry',
            defaults={
                'description': 'Basic chemistry concepts including atomic structure, periodic table, and chemical reactions',
                'order': 2
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created topic: {chemistry.title}'))

        # Create sample Chemistry note
        chemistry_notes = [
            {
                'title': 'Periodic Table and Elements',
                'content': '''<h3>The Periodic Table</h3>
<p>The periodic table organizes all known chemical elements based on their atomic number, electron configuration, and recurring chemical properties.</p>
<h4>Key Features:</h4>
<ul>
<li><strong>Groups:</strong> Vertical columns (1-18)</li>
<li><strong>Periods:</strong> Horizontal rows (1-7)</li>
<li><strong>Metals, Non-metals, Metalloids</strong></li>
</ul>
<h4>Important Groups:</h4>
<ul>
<li>Group 1: Alkali Metals (Li, Na, K)</li>
<li>Group 17: Halogens (F, Cl, Br)</li>
<li>Group 18: Noble Gases (He, Ne, Ar)</li>
</ul>''',
                'key_points': '''• 118 elements in the periodic table
• Arranged by atomic number
• Groups show similar chemical properties
• Periods show electron shell filling
• Metals on left, non-metals on right''',
                'exam_tips': '''<p><strong>Must Remember:</strong></p>
<ul>
<li>First 20 elements and their symbols</li>
<li>Group names and properties</li>
<li>Periodic trends (atomic size, electronegativity)</li>
</ul>''',
                'common_mistakes': '''• Confusing groups with periods
• Not remembering element symbols
• Mixing up metal and non-metal properties''',
                'difficulty_level': 'easy',
                'importance_rating': 5,
                'estimated_read_time': 6,
                'tags': ['Important', 'Basic Concept', 'Frequently Asked']
            }
        ]

        for note_data in chemistry_notes:
            tag_names = note_data.pop('tags', [])
            note, created = Note.objects.get_or_create(
                topic=chemistry,
                title=note_data['title'],
                defaults=note_data
            )
            if created:
                for tag_name in tag_names:
                    if tag_name in tags:
                        note.tags.add(tags[tag_name])
                self.stdout.write(self.style.SUCCESS(f'Created note: {note.title}'))

        # Create Biology Topic
        biology, created = Topic.objects.get_or_create(
            subject=science,
            title='Biology',
            defaults={
                'description': 'Life sciences covering cell biology, human anatomy, and ecology',
                'order': 3
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created topic: {biology.title}'))

        # Create sample Biology note
        biology_notes = [
            {
                'title': 'Cell Structure and Function',
                'content': '''<h3>The Cell - Basic Unit of Life</h3>
<p>All living organisms are made up of cells. There are two main types:</p>
<h4>Prokaryotic Cells:</h4>
<ul>
<li>No nucleus</li>
<li>Simple structure</li>
<li>Example: Bacteria</li>
</ul>
<h4>Eukaryotic Cells:</h4>
<ul>
<li>Have nucleus</li>
<li>Complex organelles</li>
<li>Example: Plant and animal cells</li>
</ul>
<h4>Important Organelles:</h4>
<ul>
<li><strong>Nucleus:</strong> Control center, contains DNA</li>
<li><strong>Mitochondria:</strong> Powerhouse of the cell</li>
<li><strong>Ribosomes:</strong> Protein synthesis</li>
<li><strong>Chloroplasts:</strong> Photosynthesis (plants only)</li>
</ul>''',
                'key_points': '''• Cell is the basic unit of life
• Two types: Prokaryotic and Eukaryotic
• Nucleus contains genetic material (DNA)
• Mitochondria produces energy (ATP)
• Plant cells have cell wall and chloroplasts''',
                'exam_tips': '''<p><strong>Focus on:</strong></p>
<ul>
<li>Differences between plant and animal cells</li>
<li>Functions of major organelles</li>
<li>Cell division (mitosis and meiosis)</li>
</ul>''',
                'common_mistakes': '''• Confusing prokaryotic with eukaryotic
• Not knowing organelle functions
• Forgetting plant-specific structures''',
                'difficulty_level': 'easy',
                'importance_rating': 5,
                'estimated_read_time': 7,
                'tags': ['Important', 'Basic Concept', 'Frequently Asked']
            }
        ]

        for note_data in biology_notes:
            tag_names = note_data.pop('tags', [])
            note, created = Note.objects.get_or_create(
                topic=biology,
                title=note_data['title'],
                defaults=note_data
            )
            if created:
                for tag_name in tag_names:
                    if tag_name in tags:
                        note.tags.add(tags[tag_name])
                self.stdout.write(self.style.SUCCESS(f'Created note: {note.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated Science data!'))

# Made with Bob
