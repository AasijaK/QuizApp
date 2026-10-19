from django import forms
from django.contrib.auth.models import User
from .models import Question, Subject

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            'subject',
            'topic',
            'question_text',
            'option1',
            'option2',
            'option3',
            'option4',
            'correct_answer',
            'explanation',
            'difficulty'
        ]

        widgets = {
            'question_text': forms.Textarea(
                attrs={'rows': 4}
            ),

            'explanation': forms.Textarea(
                attrs={'rows': 3}
            ),

            'correct_answer': forms.Select(
                choices=[
                    ('1', 'Option 1'),
                    ('2', 'Option 2'),
                    ('3', 'Option 3'),
                    ('4', 'Option 4')
                ]
            )
        }

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = [
            'name',
            'description'
        ]