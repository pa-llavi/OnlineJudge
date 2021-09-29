from .models import Problem, TestCase, Submission
from .runcodes import judge_gcc, judge_gpp, judge_python

def run_tc(submission: Submission):
    if submission.lang == Submission.GCC:
        output = judge_gcc(submission)
    elif submission.lang == Submission.GPP:
        output = judge_gpp(submission)
    elif submission.lang == Submission.PYTHON:
        output = judge_python(submission)

    submission.verdict = output['verdict']
    submission.save()
