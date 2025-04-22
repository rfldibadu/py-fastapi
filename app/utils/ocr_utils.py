from google.cloud import vision
from typing import List, Tuple

def extract_text_from_image_bytes(image_bytes: bytes) -> List[str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image) # type: ignore

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    return [text.description for text in response.text_annotations]
