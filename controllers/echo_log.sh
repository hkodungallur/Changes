#!/bin/bash
# assumes it is running in a git repository
# Arguments:
#    date in form YYYY-MM-DD


logs=$(git log --since="$1 0:00:00 PDT" --before="$1 23:59:59 PDT")
if [ "x$logs" != "x" ]; then
    echo Project: $REPO_PROJECT 
    echo
    git log --since="$1 0:00:00 PDT" --before="$1 23:59:59 PDT" | sed 's/^/    /'
    echo
    echo
fi
