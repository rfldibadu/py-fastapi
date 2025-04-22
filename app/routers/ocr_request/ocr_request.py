from fastapi import APIRouter, UploadFile, File, HTTPException
from google.cloud import vision
from uuid import uuid4
import os

router = APIRouter()

# Optional: Directory to store uploaded images (toggle this with SAVE_IMAGE)
SAVE_IMAGE = False
UPLOAD_DIR = "uploads/ocr"
if SAVE_IMAGE:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ocr/local")
async def detect_text_from_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Optional: Save file to disk for debugging/history
        if SAVE_IMAGE:
            filename = f"{uuid4().hex}_{file.filename}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(contents)

        # Initialize the Vision client
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=contents)

        # Perform OCR
        response = client.text_detection(image=image)  # type: ignore

        if response.error.message:
            raise HTTPException(status_code=500, detail=response.error.message)

        # Extract and format the detected text
        result = []
        for text in response.text_annotations:
            result.append({
                "text": text.description,
                "bounds": [
                    {"x": v.x, "y": v.y} for v in text.bounding_poly.vertices
                ]
            })

        return {
            "success": True,
            "message": "Text extracted successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
