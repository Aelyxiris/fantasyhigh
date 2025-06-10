# Local Installation Instructions

Hello and welcome to the wonderful world of perfect markdown websites! Let's start with the installation process.

## Dependency Installation

### Dependencies

- VSCode
- Git
- GitHub (on web)
- GitHub CLI
- Python (I recommend 3.12)
- Python for VSCode Extension
- LaTeX Workshop
- Various Python Packages

If you already have some of these installed, great! Feel free to skip those sections. Otherwise let's-a go!

### VSCode

Install VSCode here: https://code.visualstudio.com/download.

### Git

You'll want to install git first which is useful for a lot of things.
If you're on windows, go here: [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)
and download it.

If you're on mac, simply open your terminal and type the following:

```bash
git --version
```
and it should prompt you to install it.

In the installation instructions, everything default is fine except for these line items!

- Default editor &rarr; Choose VSCode
- Default branch name &rarr; Choose "main" (second option)
Not sure if these show up on mac, shouldn't matter.

Then type:
```
git config --global user.email "youremail@example.com"
git config --global user.name "nickname"
```
Of course replacing with your email and whatever preferred name.

### GitHub

Go to github.com and make an account. 

### GitHub CLI

Download the GitHub CLI here: https://cli.github.com/
Open the downloaded file to install it.

Then, in your terminal, type
```
gh auth login
```
Follow the prompts to login to your github account. 
Select HTTPS when prompted for preferred protocol (press enter).
When asked if you would like to authenticate to Git with your GitHub credentials, enter Y.
Follow the associated instructions.

### Python

Go to https://www.python.org/downloads/release/python-31210/ and install the appropriate release. AND CLICK THE
VERY IMPORTANT BOX LABELED "Add Python.exe to PATH."

### Python for VSCode

Open the marketplace (4 weird squares on the left) tab in VSCode. Install the "Python" extension (description: Python language support).

### Website Installation

First create a folder somewhere, maybe like "RPG" or "Programming" or something in your Documents (whatever, your choice).
Then, open your powershell (windows) or terminal (mac) and using cd commands navigate to that folder.
(For instance, it might start you in your main users folder so you may have to type)
```
cd Documents
cd RPG
```
You should be able to find what folders are within your folder by typing `ls`. You can also type `cd ..` if you made a mistake and want to go back.

Then, assuming you've done everything right, simply type:
```
git clone https://github.com/Aelyxiris/fantasyhigh.git
```

Now, open VSCode, and go File -> Open and click on the new folder that was created.

### Python Dependency Installation

Once open in that folder in VSCode, hit CTRL+~ or CMD+~ if mac and create a virtual environment and install packages in it (copy individually):
```
python -m venv fantasyhigh
```
Now, press CTRL+SHIFT+P (windows) or CMD+SHIFT+P (mac) and type `Python: Select Interpreter` (it should pop up in suggestions, click it).
After clicking, you should see something like "python 3.12.3: ('fantasyhigh': venv)" and click that.

Click in the menu bar "Terminal -> New Terminal" (may be hidden).
Type:
```
pip install -r requirements.txt
```

### Usage

Whenever you want to use it press CTRL+~ or CMD+~ (win or mac) and type:
```
mkdocs serve
```
This will put a url in the terminal which you can CTRL+click to open in your browser which opens a local copy of the website. You can then make changes in the files 
under docs -> [filename].md and it'll auto propagate to the local copy of the website.

You can also make new pages by duplicating existing .md files, or creating more, and adding them to the nav under "mkdocs.yml" (follow the pattern there).

Markdown usage instructions can be looked up online.

## Git Usage

If someone else has made changes to the repo, type git pull.
