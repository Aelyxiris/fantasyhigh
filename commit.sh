#!/bin/sh

echo "Please enter your commit message:"
read commit_message

git add .
git commit -m "$commit_message"

echo "Select the branch to push:"
git branch
read branch_name

git push -u origin $branch_name