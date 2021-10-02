from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import subprocess as sb
from multiprocessing import Process
from time import time

from .models import Problem, TestCase, Submission
from .runcodes import judge_gcc, judge_gpp, judge_python

# from . import run_tc
# Create your views here.


def run_tc(submission: Submission):
    if submission.lang == Submission.GCC:
        output = judge_gcc(submission)
    elif submission.lang == Submission.GPP:
        output = judge_gpp(submission)
    elif submission.lang == Submission.PYTHON:
        output = judge_python(submission)

    submission.verdict = output['verdict']
    submission.save()


@login_required(login_url='login_n')
def problem(request,prob_id):
    problem = Problem.objects.get(id = prob_id)

    if request.method == 'POST':
        submission = Submission(user=request.user, problem=problem, code=request.POST['code'], lang=request.POST['language'])
        submission.save()
        run_tc(submission)
        # if __name__ == "problem.views":
        #     pro = Process(target=run_tc, args=(submission,))
        #     pro.start()
        return redirect('submissions')

    sampleTC =  TestCase.objects.filter(problem_id=problem.id, show=True)
    context = {
        'problem': problem,
        'samples': sampleTC,
        'langs': Submission.LANG,
    }
    return render(request, 'problem.html', context)


@login_required(login_url='login_n')
def submissions(request):
    if request.method == 'POST':
        pass
    context = {
        'submissions': Submission.objects.all(),
    }
    return render(request, 'submissions.html', context)