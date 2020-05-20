#! /bin/bash
message=${1}

git status
sleep 5s;
git add .travis.yml
git add Source/*.py;
git add *.sh;
git commit -m "$message";
branchName=$(git rev-parse --abbrev-ref HEAD);

git push origin $branchName


