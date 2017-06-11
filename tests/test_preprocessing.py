import logging
from os import path
from unittest import TestCase
from PIL import Image
from octopus.preprocessing import process


class Preprocessing(TestCase):
    def test_text(self):
        sample_text = '''부산여행중 충전걱정 안하고 다니는 중.
        공영주차장에 신형 급속충전기가 짠~
        시험운영중이라 공짜에 성능도 좋아서 대만족.
        예전에 부산왔을때 정말 맛있게 먹은 밀면 집이 있어서 왔는데 대기 팀수가
        평균 70팀... 지난번엔 대기없이 그냥 먹어서 그냥 밀면집인가보다 했는데
        맛집이었어.... ㄷㄷ#전기차 #테슬라 #tesla #p85d #차스타그램 #카스타그램
        #해운대맛집 #해운대가야밀면 #밀면'''
        result = process(sample_text)
        logging.getLogger().warning(result)
        for word in ['부산', '여행', '전기차',
                     '충전', '만족', '주차장', '밀면']:
            self.assertIn(word, result)

    def test_image(self):
        cat = Image.open(path.join(path.dirname(__file__),
                                   'data/tabby-cat.jpg'))
        result = process(cat)
        logging.getLogger().warning(result)
        self.assertIn('tabby', result)
