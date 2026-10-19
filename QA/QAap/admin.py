from django.contrib import admin
from .models import Profile, Subject, Question, QuizResult

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'subject',
        'difficulty',
        'contributor'
    )

    list_filter = (
        'subject',
        'difficulty'
    )

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'total_questions',
        'correct_answers',
        'score',
        'attempted_at'
    )