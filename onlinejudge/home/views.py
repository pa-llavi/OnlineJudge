from django.shortcuts import render
from problem.models import Problem

# Create your views here.

def problems(request) :
    context = {
        'problems' : Problem.objects.all()
    }
    #return HttpResponse('<h1>Home</h1>')
    return render(request, 'problems.html', context)
