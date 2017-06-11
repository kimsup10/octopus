import jpype
from . import process

try:
    from konlpy.tag import Mecab
    HA = Mecab()
except Exception:
    from konlpy.tag import Kkma
    HA = Kkma()


@process.register(str)
def process(text):
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()
    try:
        tokens = HA.nouns(text)
        tokens.extend(filter(lambda w: w.startswith('#'),
                             text.split()))
        return tokens
    except Exception:
        return text.split()
