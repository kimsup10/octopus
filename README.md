Octopus
=======
Paul, the octopus

- 환경설정하는 방법
```bash
# Install Selenium Chrome Driver
brew install chromedriver

git clone git@github.com:huntrax11/octopus.git
cd octopus
# Create Virtual Environment
pyvenv env

# Activate virtual environment
source env/bin/activate
python setup.py develop

# Run unittest
python -m unittest

# Deactivate virtual environment
deactivate
```
