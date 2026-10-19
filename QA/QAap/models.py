from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return self.user.username

class Subject(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):

    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=1)

    explanation = models.TextField(blank=True)

    topic = models.CharField(max_length=100, blank=True)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Medium'
    )

    contributor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class QuizResult(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    total_questions = models.IntegerField()

    correct_answers = models.IntegerField()

    wrong_answers = models.IntegerField()

    score = models.FloatField()

    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.score}%"