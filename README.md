Octopus
=======
Paul, the octopus

- 환경설정하는 방법
```bash
# Install Selenium Chrome Driver
brew install chromedriver
# (Optional) Install mecab for better NLP
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
# (Optional) Install tensorflw-gpu for faster CV
sed -i '.bak' 's/^tensorflow$/tensorflow-gpu/' requirements.txt


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
