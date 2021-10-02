import subprocess as sp
from time import time

from .models import Problem, Submission

CODES_DIR = 'codes\\'

def judge_python(submission: Submission):
    file_name = str(submission.id)
    
    file = open(CODES_DIR + file_name + '.py', 'x') #create new file for code
    file.write(submission.code)
    file.close()

    def delete_file():
        sp.run(['del', '{}{}.py'.format(CODES_DIR, file_name)], shell=True)
    
    for tc in submission.problem.testcase_set.all():
        start = time()
        try:
            x = sp.run(['python', '{}{}.py'.format(CODES_DIR, file_name)] ,input=tc.input.encode() ,capture_output=True ,timeout=submission.problem.time_limit)
        except sp.TimeoutExpired:
            delete_file()
            return {'verdict':'TLE', 'time': (time()-start)*1000}

        runtime = time() - start 
        if  x.returncode != 0:
            delete_file()
            print(x.stderr.decode())
            return {'verdict': 'RE', 'time':runtime*1000}

        user_op = x.stdout.decode().strip().rstrip("\n").strip()
        if user_op != tc.output:
            delete_file()
            return {'verdict': 'WA', 'time': runtime}
    
    delete_file()
    return {'verdict': 'AC', 'time': runtime}



def judge_gcc(submission : Submission):
    return __judge_gxx(submission, 'gcc', 'c')

def judge_gpp(submission : Submission):
    return __judge_gxx(submission, 'g++', 'cpp')


def __judge_gxx(submission: Submission, compiler, ext):
    filename = str(submission.id)

    file = open(CODES_DIR + filename + '.{}'.format(ext), 'xt')
    file.write(submission.code)
    file.close()

    # Compile
    x = sp.run([compiler, '-o', CODES_DIR + filename, '{}{}.{}'.format(CODES_DIR, filename, ext)])
    # Delete code file
    sp.run(['del', '{}{}.{}'.format(CODES_DIR, filename, ext)], shell=True)

    def delete_file():
        sp.run(['del', '{}{}'.format(CODES_DIR, filename)], shell=True)
    
    if(x.returncode != 0):
        return {'verdict': 'CE', 'time': 0}

    maxtime = 0.0
    for tc in submission.problem.testcase_set.all():
        start = time()
        try:
            x = sp.run('{}{}'.format(CODES_DIR, filename), input=tc.input.encode(), capture_output=True, timeout=submission.problem.time_limit)
        except sp.TimeoutExpired:
            delete_file()
            return {'verdict': 'TLE', 'time': (time() - start) * 1000}
        
        runtime = time() - start 

        if cp.returncode != 0:
            # delete_file()
            return {'verdict': 'RE', 'time': runtime}

        useroutput = x.stdout.decode().strip().rstrip("\n").strip()
        if useroutput != tc.output:
            # delete_file()
            return {'verdict': 'WA', 'time': runtime}
    
    # delete_file()
    return {'verdict': 'AC', 'time': runtime}
