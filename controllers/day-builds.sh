#!/bin/bash

# Assumes it is being run in a repo checkout
# Also assumes build-team-manifests is synced into top-level directory
# And asssumes both repo and build-team-manifests are up-to-date

# Arguments:
#    date in form YYYY-MM-DD
#    product branch (default: master)

day=$1
branch=${2-sherlock-4.0.0}
cd build-team-manifests
git checkout $branch > /dev/null 2>&1
lastofday=`git log --before "$day 23:59:59 PDT" -1 --format=%H`
priorday=`git log --before "$day 0:00:00 PDT" -1 --format=%H`
git show $lastofday:sherlock.xml > ../lastofday.xml
git show $priorday:sherlock.xml > ../priorday.xml

echo "DIFFERENCES BETWEEN"
git log --format=%s -1 $priorday
echo "    AND"
git log --format=%s -1 $lastofday

cd ..
repo diffmanifests `pwd`/priorday.xml `pwd`/lastofday.xml
