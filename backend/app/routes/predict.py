from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.ml.predict import predict
from app.services.llm_service import generate_explanation


router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("")
async def predict_garbage(file: UploadFile = File(...)):

    try:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file")

        image_bytes = await file.read()
        import io
        from PIL import Image
        import numpy as np

        #print(type(image_bytes)) #debuging

        # Convert bytes to PIL image

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))

        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)  # batch dimension

        # Run TensorFlow prediction
        result = predict(image_array)

        llm_output = generate_explanation(result["class"])

        return {
            "class": result["class"],
            "confidence": result["confidence"],
            "description": llm_output["description"],
            "recycling_tips": llm_output["tips"]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
