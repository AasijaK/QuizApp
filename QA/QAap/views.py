from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random

from .models import Profile, Subject, Question, QuizResult
from .forms import RegisterForm, QuestionForm, SubjectForm

def home(request):

    if request.user.is_authenticated:

        if hasattr(request.user, 'profile'):

            if request.user.profile.role == 'admin':
                return redirect('admin_dashboard')

        return redirect('dashboard')

    return redirect('login')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            if hasattr(user, 'profile'):

                if user.profile.role == 'admin':
                    return redirect('admin_dashboard')

            return redirect('dashboard')

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, 'login.html')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            Profile.objects.create(
                user=user,
                role='student'
            )

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def dashboard(request):

    return render(
        request,
        'dashboard.html'
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    subjects = Subject.objects.all()

    return render(
        request,
        'AdminDB.html',
        {
            'subjects': subjects
        }
    )

@login_required
def subjects(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    subjects = Subject.objects.all()

    return render(
        request,
        'subjects.html',
        {
            'subjects': subjects
        }
    )

@login_required
def add_subject(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject added successfully."
            )

            return redirect('subjects')

    else:
        form = SubjectForm()

    return render(
        request,
        'addsub.html',
        {
            'form': form
        }
    )

@login_required
def delete_subject(request, id):

    if not request.user.is_staff:
        return redirect('dashboard')

    subject = get_object_or_404(
        Subject,
        id=id
    )

    subject.delete()

    messages.success(
        request,
        "Subject deleted."
    )

    return redirect('subjects')

@login_required
def questions(request):

    query = request.GET.get(
        'q',
        ''
    )

    subject_id = request.GET.get(
        'subject',
        ''
    )

    question_list = Question.objects.select_related(
        'subject',
        'contributor'
    )

    if query:

        question_list = question_list.filter(

            Q(question_text__icontains=query) |

            Q(topic__icontains=query) |

            Q(contributor__username__icontains=query)

        )

    if subject_id:

        question_list = question_list.filter(
            subject_id=subject_id
        )

    subjects = Subject.objects.all()

    return render(
        request,
        'questions.html',
        {
            'questions': question_list,
            'subjects': subjects,
            'query': query
        }
    )

@login_required
def add_question(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.save(
                commit=False
            )

            question.contributor = request.user

            question.save()

            messages.success(
                request,
                "Question added to collaborative bank."
            )

            return redirect('questions')

    else:
        form = QuestionForm()

    return render(
        request,
        'addque.html',
        {
            'form': form
        }
    )


@login_required
def quiz_setup(request):

    subjects = Subject.objects.all()

    return render(
        request,
        'Quizsetup.html',
        {
            'subjects': subjects
        }
    )

@login_required
def start_quiz(request):

    subject_id = request.GET.get(
        'subject'
    )

    try:

        number = int(
            request.GET.get(
                'number',
                5
            )
        )

    except ValueError:

        number = 5

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    available_questions = list(
        Question.objects.filter(
            subject=subject
        )
    )

    if len(available_questions) < number:

        messages.error(
            request,
            f"Only {len(available_questions)} questions are available."
        )

        return redirect('quiz_setup')

    selected_questions = random.sample(
        available_questions,
        number
    )

    request.session['quiz_questions'] = [
        q.id for q in selected_questions
    ]

    request.session['quiz_subject'] = subject.id

    request.session['quiz_index'] = 0

    request.session['quiz_answers'] = {}

    return redirect('quiz')

@login_required
def quiz(request):

    question_ids = request.session.get(
        'quiz_questions'
    )

    if not question_ids:
        return redirect('quiz_setup')

    index = request.session.get(
        'quiz_index',
        0
    )

    if index >= len(question_ids):

        return redirect('result')

    question = get_object_or_404(
        Question,
        id=question_ids[index]
    )

    if request.method == 'POST':

        answer = request.POST.get(
            'answer'
        )

        answers = request.session.get(
            'quiz_answers',
            {}
        )

        answers[str(question.id)] = answer

        request.session['quiz_answers'] = answers

        request.session['quiz_index'] = index + 1

        return redirect('quiz')

    return render(
        request,
        'quiz.html',
        {
            'question': question,
            'number': index + 1,
            'total': len(question_ids)
        }
    )

@login_required
def result(request):

    question_ids = request.session.get(
        'quiz_questions'
    )

    answers = request.session.get(
        'quiz_answers',
        {}
    )

    if not question_ids:
        return redirect('quiz_setup')

    questions = Question.objects.filter(
        id__in=question_ids
    )

    correct = 0

    for question in questions:

        user_answer = answers.get(
            str(question.id)
        )

        if user_answer == question.correct_answer:
            correct += 1

    total = len(question_ids)

    wrong = total - correct

    score = (
        correct / total * 100
        if total > 0
        else 0
    )

    subject = get_object_or_404(
        Subject,
        id=request.session.get(
            'quiz_subject'
        )
    )

    QuizResult.objects.create(

        student=request.user,

        subject=subject,

        total_questions=total,

        correct_answers=correct,

        wrong_answers=wrong,

        score=score

    )

    context = {

        'total': total,

        'correct': correct,

        'wrong': wrong,

        'score': score,

        'subject': subject

    }

    request.session.pop(
        'quiz_questions',
        None
    )

    request.session.pop(
        'quiz_answers',
        None
    )

    request.session.pop(
        'quiz_index',
        None
    )

    request.session.pop(
        'quiz_subject',
        None
    )

    return render(
        request,
        'result.html',
        context
    )


@login_required
def history(request):

    results = QuizResult.objects.filter(
        student=request.user
    ).order_by(
        '-attempted_at'
    )

    return render(
        request,
        'history.html',
        {
            'results': results
        }
    )