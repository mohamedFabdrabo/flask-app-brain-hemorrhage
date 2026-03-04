# Setup and Deployment Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flask-app-brain-hemorrhage.git
cd flask-app-brain-hemorrhage
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Prepare Model File

The application requires a trained YOLOv5 model file:

1. **Create models directory:**
   ```bash
   mkdir models
   ```

2. **Add your model:**
   - Place your trained model at `models/conv-model_V1.h5`
   - The model should accept 64x64 grayscale images as input
   - The model should output a single prediction value (0-1 range)

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

## Development

### Project Structure

```
flask-app-brain-hemorrhage/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── models/                     # Trained models directory
│   └── conv-model_V1.h5       # YOLOv5 model (add your model here)
├── uploads/                    # Temporary uploaded images
├── static/                     # Static files
│   ├── css/
│   │   └── main.css           # Styling
│   └── js/
│       └── main.js            # Client-side logic
└── templates/                  # HTML templates
    ├── base.html              # Base template
    └── index.html             # Main page
```

### Directory Creation

The application automatically creates the `uploads/` directory for temporary image storage.

## Configuration

### Environment Variables (Optional)

Create a `.env` file for configuration:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# Model Configuration
MODEL_PATH=models/conv-model_V1.h5
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216  # 16 MB in bytes
```

### Flask Debug Mode

**For Development:**
```bash
# In app.py, debug is enabled by default
python app.py
```

**For Production:**
- Set `debug=False` in app.py
- Use a production WSGI server (Gunicorn, uWSGI)

## Deployment

### Using Gunicorn (Recommended for Production)

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t brain-hemorrhage-detector .
docker run -p 5000:5000 brain-hemorrhage-detector
```

## Troubleshooting

### Model Not Found Error

```
Error: Model file not found at models/conv-model_V1.h5
```

**Solution:**
- Create the `models/` directory
- Ensure your model file is named exactly `conv-model_V1.h5`
- Check file path and permissions

### Port Already in Use

```
Address already in use
```

**Solution:**
```bash
# Change the port in app.py:
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use different port
```

### ModuleNotFoundError

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

### CORS Issues

If facing Cross-Origin Resource Sharing issues:

```python
from flask_cors import CORS
CORS(app)
```

Add this to app.py after creating the Flask app.

## Performance Optimization

### Prediction Speed

- Input images are resized to 64x64 pixels for efficiency
- Consider using a GPU for faster inference
- Batch processing can improve throughput

### Memory Usage

- Images are loaded and processed one at a time
- Temporary uploads are cleaned up after prediction
- Model is loaded once at startup

## Testing

### Manual Testing

1. Open browser to `http://127.0.0.1:5000/`
2. Upload a test brain scan image
3. Click "Predict!" button
4. Verify results display correctly

### Automated Testing (Optional)

Create `test_app.py`:

```python
import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest
```

## Support and Feedback

- Report issues on GitHub Issues
- Check documentation for common problems
- See CONTRIBUTING.md for contribution guidelines

## Next Steps

- [Configure your model](README.md)
- [Read the main documentation](README.md)
- [Contribute to the project](CONTRIBUTING.md)
