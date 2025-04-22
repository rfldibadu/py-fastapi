from fastapi import FastAPI
from app.routers import item_router, purchase_router
from app.routers.ocr_request import ocr_request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Register routers
app.include_router(item_router)
app.include_router(purchase_router)
app.include_router(ocr_request.router, prefix="/ocr", tags=["OCR"])

@app.get("/")
def read_root():
    return {"success": True, "message": "Server is running"}



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:3000"] if you want to limit it
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
