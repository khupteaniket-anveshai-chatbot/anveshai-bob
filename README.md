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


### 🔒 Main Branch Protection

The `main` branch is protected from accidental commits using a Git pre-commit hook.

**What happens if you try to commit to main:**
```
🚫 ERROR: Direct commits to 'main' branch are not allowed!

Please follow the proper workflow:
1. Switch to develop branch: git checkout develop
2. Make your changes and commit
3. Push to develop: git push origin develop
4. After testing, merge develop to main
```

**To bypass (not recommended):**
```bash
git commit --no-verify
```

**Protection is active:** ✅ Prevents accidental commits to main branch

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


## Server Management

### 🚀 Starting the Server

#### Method 1: Start in Terminal (Recommended)
```bash
cd /Users/aniketkhupte/Documents/AnveshAI-Updated
source venv/bin/activate
python manage.py runserver
```

The server will start on: **http://127.0.0.1:8000/**

#### Method 2: Start in Background
```bash
cd /Users/aniketkhupte/Documents/AnveshAI-Updated
source venv/bin/activate
nohup python manage.py runserver > server.log 2>&1 &
```

### 🛑 Stopping the Server

#### Method 1: If Running in Terminal
Press: **`Ctrl + C`** (or `Command + C` on Mac)

#### Method 2: If Running in Background
```bash
# Find the process
ps aux | grep "manage.py runserver" | grep -v grep

# Kill the process (replace PID with actual process ID)
kill -9 <PID>
```

#### Method 3: Quick Stop Script
```bash
# Stop all Django servers
pkill -f "manage.py runserver"
```

### 🔄 Restarting the Server

```bash
# Stop
pkill -f "manage.py runserver"

# Wait a moment
sleep 2

# Start
cd /Users/aniketkhupte/Documents/AnveshAI-Updated
source venv/bin/activate
python manage.py runserver
```

### 📋 Check Server Status

```bash
# Check if server is running
ps aux | grep "manage.py runserver" | grep -v grep

# Check which port is in use
lsof -i :8000
```

### 💡 Server Management Tips

1. **Keep Terminal Open**: When you start the server in terminal, keep that terminal window open
2. **Check Logs**: If server doesn't start, check for error messages in the terminal
3. **Port Already in Use**: If you get "port already in use" error, stop existing server first
4. **Auto-Reload**: Django automatically reloads when you change code files

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

## 📚 Importing Notes from DOCX Files

### Overview
AnveshAI includes a powerful generic DOCX import system that allows you to import study notes from Microsoft Word documents directly into the database. This system automatically parses the document structure and creates organized notes.

### File Structure
```
AnveshAI-Updated/
├── notes-source/              # Place your DOCX files here
│   └── 01. Cell.docx         # Example: Cell Biology notes
├── utils/                     # Utility modules
│   └── docx_reader.py        # DOCX reading and parsing utility
└── notes/management/commands/
    └── import_docx_notes.py  # Generic import command
```

### Prerequisites
The `python-docx` package is already included in `requirements.txt` and will be installed automatically.

### How to Import Notes

#### Step 1: Prepare Your DOCX File
1. Place your DOCX file in the `notes-source/` directory
2. Organize content with clear headings and sections
3. Use bold text or heading styles for section titles

#### Step 2: Preview Import (Dry Run)
Before importing, preview what will be imported:
```bash
python manage.py import_docx_notes "filename.docx" --dry-run
```

Example:
```bash
python manage.py import_docx_notes "01. Cell.docx" --dry-run
```

This will show:
- Number of sections found
- Preview of first 5 lines of each section
- Total paragraphs in document

#### Step 3: Import with Default Settings
```bash
python manage.py import_docx_notes "filename.docx"
```

This will:
- Create/use "Science" subject (default)
- Create topic from filename (e.g., "Cell" from "01. Cell.docx")
- Set difficulty to "medium"
- Set importance to 3 (out of 5)

#### Step 4: Import with Custom Settings
```bash
python manage.py import_docx_notes "filename.docx" \
  --subject "History" \
  --topic "Ancient India" \
  --difficulty hard \
  --importance 5
```

### Command Options

| Option | Description | Default | Choices |
|--------|-------------|---------|---------|
| `filename` | Name of DOCX file in notes-source/ | Required | - |
| `--subject` | Subject name | Science | Any string |
| `--topic` | Topic name | Filename without extension | Any string |
| `--difficulty` | Difficulty level | medium | easy, medium, hard |
| `--importance` | Importance rating | 3 | 1, 2, 3, 4, 5 |
| `--dry-run` | Preview without importing | False | - |

### Examples

**Import Cell Biology notes:**
```bash
python manage.py import_docx_notes "01. Cell.docx" \
  --subject "Science" \
  --topic "Cell Biology" \
  --importance 5
```

**Import History notes:**
```bash
python manage.py import_docx_notes "02. Ancient India.docx" \
  --subject "History" \
  --topic "Ancient Indian History" \
  --difficulty hard \
  --importance 4
```

**Preview Geography notes:**
```bash
python manage.py import_docx_notes "03. Indian Geography.docx" --dry-run
```

### What Gets Imported

For each section in your DOCX file, the system creates:
- **Title**: Section heading
- **Content**: Formatted as HTML with paragraphs, lists, and headings
- **Key Points**: Automatically extracted from bullet points and short lines
- **Tags**: Automatically tagged as "Important" and "Basic Concept" (if applicable)
- **Read Time**: Calculated based on word count (~200 words/minute)

### Viewing Imported Notes

1. Start the Django server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/`
3. Navigate to: Subject → Topic → View all notes

### Tips for Best Results

1. **Use Clear Headings**: Bold text or heading styles help identify sections
2. **Organize Content**: Group related information under headings
3. **Use Bullet Points**: They're automatically extracted as key points
4. **Keep Sections Focused**: Each section becomes a separate note
5. **Test with Dry Run**: Always preview before importing

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

## Git Workflow

### 🔑 SSH Key Configuration

**Important**: This project uses a specific SSH key for GitHub authentication.

#### SSH Key Details
- **Key Name**: `id_ed25519_anveshai`
- **Location**: `~/.ssh/id_ed25519_anveshai`
- **Public Key**: `~/.ssh/id_ed25519_anveshai.pub`
- **Email**: `khupteaniket.anveshai@gmail.com`
- **Fingerprint**: `SHA256:248IovuqBJagOMTeBrv0ck7UG1VdxSMTgWd0tTZO4N0`

#### Adding SSH Key to Agent
Before pushing to GitHub, ensure the SSH key is added to your SSH agent:

```bash
# Add the anveshai SSH key
ssh-add ~/.ssh/id_ed25519_anveshai

# Verify it's added
ssh-add -l
```

#### Using SSH Key with Git Commands
All git push/pull commands should use this specific SSH key:

```bash
# Method 1: Using GIT_SSH_COMMAND (Recommended)
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_anveshai' git push origin develop

# Method 2: Add to SSH agent first, then push normally
ssh-add ~/.ssh/id_ed25519_anveshai
git push origin develop
```

#### Troubleshooting SSH Issues

**Issue: Permission denied**
```bash
# Check if key is in SSH agent
ssh-add -l

# If not listed, add it
ssh-add ~/.ssh/id_ed25519_anveshai

# Test GitHub connection
ssh -T git@github.com
```

**Issue: Wrong key being used**
```bash
# Remove all keys from agent
ssh-add -D

# Add only the anveshai key
ssh-add ~/.ssh/id_ed25519_anveshai

# Verify
ssh-add -l
```

**Issue: Key not found**
```bash
# Check if key exists
ls -la ~/.ssh/id_ed25519_anveshai

# If missing, contact admin or regenerate key
```

### Branch Strategy

We follow a two-branch workflow:
- **`main`** - Production-ready code (stable releases only)
- **`develop`** - Development branch (active development)

### Current Branch
You are currently on: **`develop`** branch

### Working with Branches

#### Check Current Branch
```bash
git branch
```

#### Switch to Develop Branch (for development)
```bash
git checkout develop
```

#### Switch to Main Branch (for releases)
```bash
git checkout main
```

### Development Workflow

#### 1. Make Changes on Develop Branch
```bash
# Ensure you're on develop
git checkout develop

# Make your changes to files
# ...

# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to develop branch
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_anveshai' git push origin develop
```

#### 2. Merge Develop to Main (After Testing)
```bash
# Switch to main branch
git checkout main

# Merge develop into main
git merge develop

# Push to main branch
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_anveshai' git push origin main

# Switch back to develop for continued development
git checkout develop
```

### Quick Commands

#### Commit and Push to Develop
```bash
git add .
git commit -m "Your commit message"
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_anveshai' git push origin develop
```

#### View Branch Status
```bash
git status
git branch -a
```

#### View Commit History
```bash
git log --oneline --graph --all
```

---
