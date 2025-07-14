# 🖼️ Image Upscaler API

A production-ready FastAPI service for image upscaling using deep learning models with automatic fallback mechanisms, tiling support, and GPU/CPU optimization.

## 🚀 Features

- **REST API Interface**: Upload images via HTTP POST requests
- **Deep Learning Models**: Utilizes Hugging Face image-to-image pipelines
- **Smart Memory Management**: Automatically handles large images to prevent OOM errors
- **Fallback Mechanisms**: GPU → CPU fallback and model fallback support
- **Tiling Support**: Processes large images in tiles when needed
- **Cross-Origin Support**: CORS enabled for web applications
- **Comprehensive Logging**: Built-in logging for debugging and monitoring

## 📦 Project Structure

```
IMAGE_ENHANCER/
├── app.py                          # FastAPI application entry point
├── requirements.txt                # Python dependencies
├── temp_uploads/                   # Temporary uploaded files storage
├── artifacts/                      # Model artifacts and cache
├── data/                          # Data processing utilities
├── logs/                          # Application logs
└── src/
    ├── __pycache__/               # Python cache files
    ├── components/                # Core components
    │   └── image_upscaler.py      # Main upscaling logic
    ├── constants/                 # Configuration constants
    ├── entity/                    # Data entities and models
    │   ├── image_upscaler_config.py
    │   └── image_upscaler_artifact.py
    ├── exceptions/                # Custom exception handlers
    ├── logger/                    # Logging configuration
    ├── pipeline/                  # Processing pipelines
    │   └── upscaler_pipeline.py   # Main upscaling pipeline
    ├── utils/                     # Utility functions
    │   └── common_functions.py    # Tiling, resizing, memory handling
    └── venv/                      # Virtual environment
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (optional, falls back to CPU)
- 4GB+ RAM recommended

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd image-upscaler-api
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**:
   ```bash
   mkdir -p temp_uploads artifacts logs
   ```

## 🚀 Running the API

### Development Mode
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Endpoint**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📤 API Usage

### Endpoint: `POST /upscale`

Uploads and upscales an image using deep learning models.

**Request:**
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameter**: `file` (image file)

**Supported Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- TIFF (.tiff)
- BMP (.bmp)

### Example Usage

#### Using cURL:
```bash
curl -X POST "http://localhost:8000/upscale" \
  -F "file=@your_image.jpg" \
  --output upscaled_image.jpg
```

#### Using Python requests:
```python
import requests

url = "http://localhost:8000/upscale"
files = {'file': open('your_image.jpg', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('upscaled_image.jpg', 'wb') as f:
        f.write(response.content)
    print("Image upscaled successfully!")
else:
    print(f"Error: {response.status_code}")
```

#### Using JavaScript (Web):
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/upscale', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'upscaled_image.jpg';
    a.click();
});
```

## ⚙️ Configuration

The API uses configuration classes for customization:

### ImageUpscalerConfig
```python
class ImageUpscalerConfig:
    model_name: str = "default-upscaler-model"
    max_image_size: int = 1024
    tile_size: int = 512
    tile_overlap: int = 32
    output_format: str = "JPEG"
    quality: int = 95
```

### Model Fallback Chain
The system automatically tries multiple models in order:
1. Primary model (configurable)
2. `caidas/swin2SR-classical-sr-x2-64`
3. `microsoft/swin2SR-classical-sr-x2-48`

## 🧠 How It Works

1. **Image Upload**: Receives image via multipart form data
2. **Preprocessing**: Validates format and resizes if necessary
3. **Model Loading**: Loads appropriate upscaling model with fallback
4. **Processing**: Applies upscaling with tiling if needed
5. **Memory Management**: Handles GPU/CPU fallback automatically
6. **Response**: Returns upscaled image as downloadable file

## 🔧 Advanced Features

### Automatic Tiling
Large images are automatically processed in tiles to prevent memory issues:
- Configurable tile size and overlap
- Seamless tile merging
- Memory-efficient processing

### Smart Fallback
- **GPU → CPU**: Automatic fallback when GPU memory is insufficient
- **Model Fallback**: Tries alternative models if primary fails
- **Graceful Degradation**: Maintains service availability

### Logging
Comprehensive logging system tracks:
- API requests and responses
- Model loading and processing
- Error conditions and fallbacks
- Performance metrics

## 🛡️ Error Handling

The API provides detailed error responses:

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Image upscaled |
| 400 | Bad Request - Invalid file format |
| 413 | Payload Too Large - File size exceeded |
| 500 | Internal Server Error - Processing failed |

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment
- **AWS Lambda**: Serverless deployment with API Gateway
- **Google Cloud Run**: Containerized deployment
- **Heroku**: Easy deployment with git push
- **Azure Container Instances**: Scalable container deployment

## 🔒 Security Considerations

- **File Validation**: Strict image format validation
- **Size Limits**: Configurable file size limits
- **CORS**: Configurable cross-origin policies
- **Rate Limiting**: Implement rate limiting for production use
- **Input Sanitization**: Secure file handling

## 📊 Performance Tips

1. **GPU Usage**: Use CUDA-compatible GPU for faster processing
2. **Memory Management**: Adjust tile sizes based on available memory
3. **Caching**: Implement model caching for repeated requests
4. **Load Balancing**: Use multiple workers for high traffic

## 🧹 Maintenance

### Cleanup
Temporary files are stored in `temp_uploads/`. Consider:
- Regular cleanup of temporary files
- Log rotation for production environments
- Model cache management

### Monitoring
- Monitor GPU/CPU usage
- Track processing times
- Monitor disk usage for temporary files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [Issues](../../issues) section
- Review the API documentation at `/docs`
- Check logs in the `logs/` directory

---

**Built with ❤️ using FastAPI and Hugging Face Transformers**