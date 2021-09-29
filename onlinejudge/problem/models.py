from django.db import models
from django.contrib.auth.models import User
from datetime import datetime as dt

class Problem(models.Model):
    DIFF = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard')
    )

    title = models.CharField(max_length=100, unique=True)
    statement = models.TextField()
    difficulty = models.CharField(max_length=2, choices=DIFF, default='E')
    time_limit = models.IntegerField(default=1000, help_text='in milliseconds')
    def __str__(self):
        return self.title
    

class TestCase(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()
    show = models.BooleanField(default=False)


class Submission(models.Model):
    GCC = 'C'
    GPP = 'C++'
    PYTHON = 'Python'

    VERDICT = {
        ('AC', 'accepted'),
        ('WA', 'wrong answer'),
        ('TLE', 'time limit exceeded'),
        ('TT', 'testing'),
        ('RE', 'runtime error')
    }

    LANG = (
        (GCC, 'gcc'),
        (GPP, 'g++'),
        (PYTHON, 'python')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    lang = models.CharField(max_length=30, choices=LANG, default=GCC)
    verdict = models.CharField(max_length=3, choices=VERDICT, default='TT')
    submitted_at = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)
