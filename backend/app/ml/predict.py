import numpy as np
from PIL import Image
import tensorflow as tf
from app.ml.model import model
from app.ml.lables import CLASS_NAMES

IMG_SIZE = (224, 224)

def predict(image_bytes):
    
    #debug
    #print("DEBUG predict() input type:", type(image_bytes))

    preds = model.predict(image_bytes)[0]

    class_index = np.argmax(preds)
    confidence = float(preds[class_index])

    return {
        "class": CLASS_NAMES[class_index],
        "confidence": round(confidence, 2)
    }
