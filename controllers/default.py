import sys
import os
import re
import datetime
from subprocess import Popen, PIPE, STDOUT

_MYDIR = os.path.dirname(os.path.realpath(__file__))
_JIRA_PATTERN = r'(\bMB-\d+\b|\bCBD-\d+\b|\bCBSE-\d+\b)'
_REW_PATTERN = r'(http://review.couchbase.org/\d+)'

def get_log():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['repo', 'forall', '-c', '%s/echo_log.sh' %_MYDIR, sel_date]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        out1 = re.sub(_JIRA_PATTERN, r'<a href="https://issues.couchbase.com/browse/\1">\1</a>', output)
        out2 = re.sub(_REW_PATTERN, r'<a href="\1">\1</a>', out1)
        return out2
    else:
        return "No commits for %s" %sel_date

def get_diff():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['%s/day-builds.sh' %_MYDIR, sel_date]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        out1 = re.sub(_JIRA_PATTERN, r'<a href="https://issues.couchbase.com/browse/\1">\1</a>', output)
        out2 = re.sub(_REW_PATTERN, r'<a href="\1">\1</a>', out1)
        return out2
    else:
        return "No commits for %s" %sel_date

def index():
    return dict()

def flash():
    response.flash = 'this text should appear!'
    return dict()
