@echo off
setlocal

:: Prompt for commit message
set /p commit_message=Please enter your commit message: 

:: Stage all changes
git add .

:: Commit with the provided message
git commit -m "%commit_message%"

:: Show local branches
echo Select the branch to push:
git branch

:: Prompt for branch name
set /p branch_name=Enter branch name to push: 

:: Push to the selected branch
git push -u origin %branch_name%

endlocal