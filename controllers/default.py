import sys
import os
import re
import datetime
import urllib2
import json
from subprocess import Popen, PIPE, STDOUT

_MYDIR = os.path.dirname(os.path.realpath(__file__))
#_JIRA_PATTERN = r'(\bMB-\d+\b|\bCBD-\d+\b|\bCBSE-\d+\b)'
_JIRA_PATTERN = r'(\b[A-Z]+-\d+\b)'
_REW_PATTERN = r'(http://review.couchbase.org/\d+)'

def subs_url(output):
    out1 = re.sub(_JIRA_PATTERN, r'<a href="https://issues.couchbase.com/browse/\1">\1</a>', output)
    out2 = re.sub(_REW_PATTERN, r'<a href="\1">\1</a>', out1)
    return out2

def text_output(cl_dict):
    ret = ""
    for k in cl_dict.keys():
        ret = ret + "CHANGELOG for %s\n\n" %k
        val = cl_dict[k]
        for v in val:
            ret = ret + " * Commit: %s " %v.get('commitId', '')
            ret = ret + "(in build: %s)\n" %v.get('buildNum', '')
            ret = ret + "   Author: %s\n" %v.get('author', '')
            title = subs_url(v.get('title', ''))
            ret = ret + "   %s\n" %title.replace('\n', '\n   ')
            desc = subs_url(v.get('desc', ''))
            ret = ret + "   %s\n\n" %desc.replace('\n', '\n   ')

    return ret

def get_log():
    sel_branch = request.vars.branch
    sel_from = request.vars.frm
    sel_to = request.vars.to

    if not sel_from:
        return "From build# not given"
    try:
        sel_from_int = int(sel_from)
    except:
        return "From build# is not an integer"

    if not sel_to:
        return "To build# not given"
    try:
        sel_to_int = int(sel_to)
    except:
        return "To build# is not an integer"

    f = urllib2.urlopen("http://172.23.112.10:8282/changelog?from={0}&to={1}".format(sel_from, sel_to))
    ret = json.loads(f.read())
    reformat = {}
    for val in ret:
        if not reformat.has_key(val['repo']):
            reformat[val['repo']] = []
        reformat[val['repo']].append(val)
    return text_output(reformat)

def get_log_old():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['repo', 'forall', '-c', '%s/echo_log.sh' %_MYDIR, sel_date]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        return subs_url(output)
    else:
        return "No commits for %s" %sel_date

def get_diff():
    sel_date = request.vars.q
    try:
        d = datetime.datetime.strptime(sel_date, "%Y-%m-%d")
    except ValueError:
        return "Error: Invalid date"
    cmd = ['%s/day-builds.sh' %_MYDIR, sel_date, request.vars.branch]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd='/home/couchbase/couchbase')
    output = p.stdout.read()
    if output:
        return subs_url(output)
    else:
        return "No commits for %s" %sel_date

def index():
    return dict()

def flash():
    response.flash = 'this text should appear!'
    return dict()
