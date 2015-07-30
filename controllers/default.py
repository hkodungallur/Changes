import sys
import os
import datetime
from subprocess import Popen, PIPE, STDOUT

MYDIR = os.path.dirname(os.path.realpath(__file__))

def get_log():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['repo', 'forall', '-c', '%s/echo_log.sh' %MYDIR, sel_date]
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
    cmd = ['%s/day-builds.sh' %MYDIR, sel_date]
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
