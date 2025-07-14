from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import shutil
import os
import uuid
from src.pipeline.upscaler_pipeline import initialte_upscaler_pipeline
from src.logger import logging

app = FastAPI(
    title="Image Upscaler API",
    description="API to upscale images using a deep learning model with fallback and tiling",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_UPLOAD_DIR = "temp_uploads"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

@app.post("/upscale", summary="Upload and upscale an image")
async def upscale_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        # Save uploaded file
        ext = file.filename.split('.')[-1]
        temp_filename = f"{uuid.uuid4()}.{ext}"
        temp_path = os.path.join(TEMP_UPLOAD_DIR, temp_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"Image received and saved to: {temp_path}")

        # Run pipeline (returns upscaled image path)
        output_path = initialte_upscaler_pipeline(temp_path)

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Upscaling failed: output file not found.")

        logging.info(f"Upscaled image ready at: {output_path}")
        return FileResponse(output_path, media_type="image/jpeg", filename=f"upscaled_{file.filename}")

    except Exception as e:
        logging.error(f"API error during image upscaling: {e}")
        raise HTTPException(status_code=500, detail=str(e))
