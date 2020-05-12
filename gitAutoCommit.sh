#! /bin/bash
message=${0}

git status
git add Source/*;
git commit -m "$message";
branchName = $(git rev-parse --abbrev-ref HEAD);

git push origin $(branchName)


