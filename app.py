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
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_UPLOAD_DIR = "temp_uploads"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

# Strict file validation constants
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp"
}

def validate_image_file(file: UploadFile) -> None:
    """Validate that file is a supported image and within allowed size."""
    if not file.content_type or file.content_type.lower() not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only JPEG, PNG, JPG, and WEBP are allowed."
        )
    
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit."
        )

@app.post("/upscale", summary="Upload and upscale an image")
async def upscale_image(file: UploadFile = File(...)):
    try:
        # Validation
        validate_image_file(file)

        # Save file
        ext = file.filename.split('.')[-1]
        temp_filename = f"{uuid.uuid4()}.{ext}"
        temp_path = os.path.join(TEMP_UPLOAD_DIR, temp_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"Image received and saved to: {temp_path}")

        # Run upscaling pipeline
        output_path = initialte_upscaler_pipeline(temp_path)

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Upscaling failed: output file not found.")

        logging.info(f"Upscaled image ready at: {output_path}")
        return FileResponse(output_path, media_type="image/jpeg", filename=f"upscaled_{file.filename}")

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logging.error(f"API error during image upscaling: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
