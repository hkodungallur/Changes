import sys
import datetime
from subprocess import Popen, PIPE, STDOUT

def get_log():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['repo', 'forall', '-c', '/home/couchbase/couchbase/echo_log.sh', sel_date]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        return output
    else:
        return "No commits for %s" %sel_date

def get_diff():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['./day-builds.sh', sel_date]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        return output
    else:
        return "No commits for %s" %sel_date

def index():
    return dict()

def flash():
    response.flash = 'this text should appear!'
    return dict()
