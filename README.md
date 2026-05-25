# AnveshAI - MPSC Exam Preparation Platform

A comprehensive web application built with Django to help MPSC (Maharashtra Public Service Commission) aspirants prepare for their exams with exam-oriented study materials.

## Features

### Current Features (Phase 1)
- ✅ **Exam-Oriented Short Notes**: Concise, focused notes designed specifically for MPSC exams
- ✅ **Subject Organization**: Notes organized by subjects and topics
- ✅ **Advanced Filtering**: Filter notes by difficulty, importance, and tags
- ✅ **Search Functionality**: Search across all notes and topics
- ✅ **Bookmark System**: Save favorite notes using session storage
- ✅ **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- ✅ **Admin Panel**: Easy content management through Django admin
- ✅ **Hot Topics Placeholder**: Framework ready for PYQ-based hot topics

### Coming Soon (Phase 2)
- 🔄 Hot Topics based on Previous Year Questions (PYQ) analysis
- 🔄 User Authentication and Progress Tracking
- 🔄 Additional Subjects (History, Geography, Polity, Economics)
- 🔄 Practice Questions and Quizzes
- 🔄 Performance Analytics

## Technology Stack

- **Backend**: Django 6.0.5 (Python)
- **Database**: SQLite (Development), PostgreSQL-ready (Production)
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Rich Text Editor**: CKEditor
- **Template Engine**: Django Templates

## Project Structure

```
AnveshAI-Updated/
├── anveshai_project/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── notes/                     # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # URL routing
│   └── management/           # Custom management commands
│       └── commands/
│           └── populate_science_data.py
├── templates/                 # HTML templates
│   ├── base.html
│   └── notes/
│       ├── home.html
│       ├── subject_detail.html
│       ├── topic_detail.html
│       ├── note_detail.html
│       ├── search_results.html
│       ├── bookmarks.html
│       ├── hot_topics.html
│       ├── about.html
│       └── how_to_use.html
├── static/                    # Static files (CSS, JS, Images)
├── media/                     # User uploaded files
├── requirements.txt           # Python dependencies
└── manage.py                 # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Navigate to Project Directory
```bash
cd /Users/aniketkhupte/Documents/AnveshAI-Updated
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (if not already created)
```bash
python manage.py createsuperuser
```
**Default credentials (already created):**
- Username: `admin`
- Password: `admin123`
- Email: `admin@anveshai.com`

### Step 6: (Optional) Populate Sample Data
```bash
python manage.py populate_science_data
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## Usage Guide

### For Administrators

#### Accessing Admin Panel
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with admin credentials
3. Manage Subjects, Topics, Notes, Tags, and Hot Topics

#### Adding New Content

**Adding a Subject:**
1. Go to Admin → Subjects → Add Subject
2. Fill in: Name, Description, Icon (Font Awesome class), Order
3. Save

**Adding a Topic:**
1. Go to Admin → Topics → Add Topic
2. Select Subject, enter Title, Description, Order
3. Save

**Adding a Note:**
1. Go to Admin → Notes → Add Note
2. Fill in all fields:
   - Select Topic
   - Enter Title
   - Add Content (use rich text editor)
   - Add Key Points (bullet points for quick revision)
   - Add Exam Tips (strategies and tricks)
   - Add Common Mistakes (what to avoid)
   - Set Difficulty Level (Easy/Medium/Hard)
   - Set Importance Rating (1-5 stars)
   - Set Estimated Read Time
   - Select Tags
3. Save

**Adding Tags:**
1. Go to Admin → Tags → Add Tag
2. Enter Name and Color (hex code)
3. Save

### For Students

#### Browsing Notes
1. Visit home page
2. Click on a subject (e.g., Science)
3. Select a topic (e.g., Physics)
4. Browse notes or use filters

#### Using Filters
- Filter by Difficulty: Easy, Medium, Hard
- Filter by Importance: 1-5 stars
- Filter by Tags: Specific categories

#### Searching
1. Use search bar in navigation or home page
2. Enter keywords
3. Apply additional filters if needed

#### Bookmarking
1. Open any note
2. Click "Bookmark" button
3. Access bookmarks from navigation menu

## Database Models

### Subject
- Represents main subjects (Science, History, etc.)
- Fields: name, description, icon, order, is_active

### Topic
- Represents topics within subjects (Physics, Chemistry, etc.)
- Fields: subject (FK), title, description, order, is_active

### Note
- Individual study notes
- Fields: topic (FK), title, content, key_points, exam_tips, common_mistakes, difficulty_level, importance_rating, tags (M2M)

### Tag
- Categorization tags
- Fields: name, color

### HotTopic
- PYQ-based hot topics (future feature)
- Fields: subject (FK), title, description, frequency, last_appeared_year, related_notes (M2M)

## API Endpoints (Views)

- `/` - Home page
- `/subject/<slug>/` - Subject detail
- `/subject/<subject_slug>/<topic_slug>/` - Topic detail with notes
- `/subject/<subject_slug>/<topic_slug>/<note_slug>/` - Note detail
- `/search/` - Search notes
- `/bookmarks/` - View bookmarked notes
- `/bookmark/toggle/<note_id>/` - Toggle bookmark
- `/hot-topics/` - Hot topics list
- `/about/` - About page
- `/how-to-use/` - How to use guide

## Adding Your Own Notes

### Method 1: Using Admin Panel (Recommended)
1. Login to admin panel
2. Navigate to Notes → Add Note
3. Fill in all required fields
4. Use the rich text editor for formatting
5. Save

### Method 2: Using Management Command
1. Edit `notes/management/commands/populate_science_data.py`
2. Add your note data in the appropriate section
3. Run: `python manage.py populate_science_data`

### Method 3: Programmatically
```python
from notes.models import Subject, Topic, Note, Tag

# Get or create subject and topic
subject = Subject.objects.get(name='Science')
topic = Topic.objects.get(title='Physics', subject=subject)

# Create note
note = Note.objects.create(
    topic=topic,
    title='Your Note Title',
    content='<p>Your content here</p>',
    key_points='• Point 1\n• Point 2',
    exam_tips='<p>Tips here</p>',
    difficulty_level='medium',
    importance_rating=4,
    estimated_read_time=5
)

# Add tags
tag = Tag.objects.get(name='Important')
note.tags.add(tag)
```

## Deployment

### For Production

1. **Update Settings:**
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Use environment variables for SECRET_KEY
   - Configure PostgreSQL database

2. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Use Production Server:**
   - Gunicorn, uWSGI, or similar
   - Configure Nginx/Apache

4. **Security Checklist:**
   - Enable HTTPS
   - Set secure cookies
   - Configure CSRF settings
   - Use strong SECRET_KEY

## Troubleshooting

### Common Issues

**Issue: Admin CSS not loading**
```bash
python manage.py collectstatic
```

**Issue: Database errors**
```bash
python manage.py migrate
```

**Issue: Import errors**
```bash
pip install -r requirements.txt
```

## Contributing

When adding new notes:
1. Ensure content is exam-oriented
2. Include key points for quick revision
3. Add exam tips and common mistakes
4. Set appropriate difficulty and importance
5. Use relevant tags

## Future Enhancements

- [ ] PYQ integration and analysis
- [ ] User authentication system
- [ ] Progress tracking
- [ ] More subjects (History, Geography, Polity, Economics)
- [ ] Practice questions
- [ ] Mock tests
- [ ] Performance analytics
- [ ] Mobile app

## Support

For issues or questions:
- Check the "How to Use" page in the application
- Review this README
- Contact: admin@anveshai.com

## License

This project is for educational purposes.

---

**Version:** 1.0.0  
**Last Updated:** May 2024  
**Developed for:** MPSC Aspirants