import tensorflow as tf

MODEL_PATH = "model/garbage_classifier.h5"

model = tf.keras.models.load_model(MODEL_PATH)
