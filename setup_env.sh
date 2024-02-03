#!/bin/bash
VERSION=0.1

python3 -m venv venv
echo Created virtual environment as \'venv/\'

source venv/bin/activate
echo Activated virtual environment.

pip install --upgrade pip

# if requirements already, do this
if test -f requirements.txt
then
  echo requirements.txt found, installing from it.;
  pip install -r requirements.txt
else
  echo No requirements.txt found, creating an empty one. You will have to add them after you populate the environment with pip.
  touch requirements.txt
fi

# -n is no newline
echo -n "Install jupyter notebook into this environment?[y/n] "
read -r NOTEBAE
if [[ $NOTEBAE = "y" ]]
then
  echo -n "What name for jupyter kernel? "
  read -r KERNELNAME
  echo installing ipykernel and adding it to requirements
  pip install ipykernel
  python3 -m ipykernel install --user --name="$KERNELNAME"
  echo Installed kernel for virtual environment \'"$KERNELNAME"/\'
  export ipk_version=$(pip freeze | grep ipykernel)
  #disable shellcheck for assignment in pycharm
  # shellcheck disable=SC2154
  echo "$ipk_version and its dependencies installed and added to requirements."
#  echo "$ipk_version" >> requirements.txt
  pip freeze >> requirements.txt
  echo "Jupyter installed. Launch with \'jupyter notebook\'"
else
  echo "No jupyter environment installed, use [-j|--jupyter] to add it."
fi


#.gitignore template
read -r -d '\n' ignore_template << EndOfText
### pycharm python template
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

### vscode python template
.DS_Store
.huskyrc.json
out
log.log
**/node_modules
*.pyc
*.vsix
envVars.txt
**/.vscode/.ropeproject/**
**/testFiles/**/.cache/**
*.noseids
.nyc_output
.vscode-test
__pycache__
npm-debug.log
**/.mypy_cache/**
!yarn.lock
coverage/
cucumber-report.json
**/.vscode-test/**
**/.vscode test/**
**/.vscode-smoke/**
**/.venv*/
port.txt
precommit.hook
pythonFiles/lib/**
pythonFiles/get-pip.py
debug_coverage*/**
languageServer/**
languageServer.*/**
bin/**
obj/**
.pytest_cache
tmp/**
.python-version
.vs/
test-results*.xml
xunit-test-results.xml
build/ci/performance/performance-results.json
!build/
debug*.log
debugpy*.log
pydevd*.log
nodeLanguageServer/**
nodeLanguageServer.*/**
dist/**
# translation files
*.xlf
package.nls.*.json
l10n/

### jupyter notebook python template
*.bundle.*
lib/
node_modules/
*.egg-info/
.ipynb_checkpoints
*.tsbuildinfo

# Created by https://www.gitignore.io/api/python
# Edit at https://www.gitignore.io/?templates=python

### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# Mr Developer
.mr.developer.cfg
.project
.pydevproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# OS X stuff
*.DS_Store

# End of https://www.gitignore.io/api/python

_temp_extension
junit.xml
[uU]ntitled*
notebook/static/*
!notebook/static/favicons
notebook/labextension
notebook/schemas
docs/source/changelog.md
docs/source/contributing.md

# playwright
ui-tests/test-results
ui-tests/playwright-report

# VSCode
.vscode

# RTC
.jupyter_ystore.db

# yarn >=2.x local files
.yarn/*
.pnp.*
ui-tests/.yarn/*
ui-tests/.pnp.*
EndOfText

touch .gitignore
echo "$ignore_template" >> .gitignore
echo Created .gitignore with python templates from pycharm, vscode, and jupyter.

mkdir notebooks
mkdir modules
touch README.md
echo "$VERSION" >> README.md
touch __init__.py
echo Python project directory structure built.
echo Next steps:
echo Activate the virtual environment with \'source venv/bin/activate\'
echo Then, initialize the git repository and connect it to the remote.
echo Done.
