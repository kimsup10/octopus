from . import process
try:
    from konlpy.tag import Mecab
    HA = Mecab()
except Exception:
    from konlpy.tag import Kkma
    HA = Kkma()


@process.register(str)
def process(text):
    try:
        return HA.nouns(text)
    except Exception:
        return text.split()
