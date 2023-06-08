# importing libraries
from fastapi import FastAPI, File, UploadFile
import numpy as np
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf

# loading model
model = tf.keras.models.load_model('../notebooks/saved_models/model_2023-05-18_13-55-21')

class_name = ['Early Blight', 'Late Blight', 'Healthy']

app = FastAPI()

# reading and reshaping an image model has been trained on (180, 180) img size
def read_img(data):
    try:
        img = Image.open(BytesIO(data))
    except Exception as e:
        raise ValueError(f"Failed to open image: {e}")
    img = img.resize((180, 180))
    img = np.array(img)
    return img


@app.post('/analysis')
async def pred(file: UploadFile = File(...)):
    img = read_img(await file.read())

    img_reshape = np.expand_dims(img, 0)

    if img_reshape is None:
        raise ValueError("Image could not be reshaped")

    pred = model.predict(img_reshape)
    pred_class = class_name[np.argmax(pred)]
    confidence = float(np.max(pred))
    return {
        'prediction': pred_class,
        'confidence': confidence
    }
