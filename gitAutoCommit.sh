#! /bin/bash
message=${0}

git status
sleep 5s;
git add Source/*;
git add *.sh;
git commit -m "$message";
branchName=$(git rev-parse --abbrev-ref HEAD);

git push origin $branchName


