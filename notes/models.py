from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Subject(models.Model):
    """Model for subjects like Science, History, Geography, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_topics_count(self):
        return self.topics.count()

    def get_notes_count(self):
        return Note.objects.filter(topic__subject=self).count()


class Topic(models.Model):
    """Model for topics within a subject (e.g., Physics, Chemistry under Science)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order within subject")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['subject', 'order', 'title']
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        unique_together = ['subject', 'slug']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name} - {self.title}"

    def get_notes_count(self):
        return self.notes.filter(is_published=True).count()


class Tag(models.Model):
    """Model for tags to categorize notes"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Note(models.Model):
    """Model for individual study notes"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    IMPORTANCE_CHOICES = [
        (1, '⭐ Low'),
        (2, '⭐⭐ Medium'),
        (3, '⭐⭐⭐ High'),
        (4, '⭐⭐⭐⭐ Very High'),
        (5, '⭐⭐⭐⭐⭐ Critical'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, blank=True)
    
    # Content fields
    content = RichTextField(help_text="Main content of the note")
    key_points = models.TextField(blank=True, help_text="Bullet points of key concepts")
    exam_tips = RichTextField(blank=True, help_text="Exam-specific tips and tricks")
    common_mistakes = models.TextField(blank=True, help_text="Common mistakes to avoid")
    
    # Metadata
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    importance_rating = models.IntegerField(choices=IMPORTANCE_CHOICES, default=3)
    estimated_read_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Relationships
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')
    
    # Status
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-importance_rating', 'topic', 'title']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        unique_together = ['topic', 'slug']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_difficulty_badge_class(self):
        """Return Bootstrap badge class based on difficulty"""
        badges = {
            'easy': 'success',
            'medium': 'warning',
            'hard': 'danger',
        }
        return badges.get(self.difficulty_level, 'secondary')

    def get_importance_stars(self):
        """Return star rating as string"""
        return '⭐' * self.importance_rating


class HotTopic(models.Model):
    """Model for hot topics based on PYQ analysis (future feature)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='hot_topics')
    title = models.CharField(max_length=200)
    description = models.TextField()
    frequency = models.IntegerField(default=0, help_text="Number of times appeared in PYQs")
    last_appeared_year = models.IntegerField(blank=True, null=True)
    related_notes = models.ManyToManyField(Note, blank=True, related_name='hot_topics')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-frequency', '-last_appeared_year']
        verbose_name = 'Hot Topic'
        verbose_name_plural = 'Hot Topics'

    def __str__(self):
        return f"{self.subject.name} - {self.title}"

# Made with Bob
