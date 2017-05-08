from operator import itemgetter
import numpy as np
from PIL.Image import Image
from keras.preprocessing import image
from keras.applications.resnet50 import (ResNet50,
                                         preprocess_input,
                                         decode_predictions)
from . import process


model = ResNet50(weights='imagenet')


@process.register(Image)
def process(img):
    X = image.img_to_array(img.resize((224, 224)))
    X = np.expand_dims(X, axis=0)
    X = preprocess_input(X)
    preds = model.predict(X)
    result = decode_predictions(preds, top=3)[0]
    return list(map(itemgetter(1), result))
