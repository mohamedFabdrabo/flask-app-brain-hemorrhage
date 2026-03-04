# Brain Hemorrhage Detection - YOLOv5 Web Interface

A Flask-based web application for detecting brain hemorrhages using a trained YOLOv5 deep learning model. Upload medical images and get instant predictions with visual feedback.

## Features

-  **Image Upload Interface** - Clean, intuitive UI for uploading medical images
-  **ML-Powered Detection** - Uses trained YOLOv5 model for brain hemorrhage detection
-  **Real-time Predictions** - Get instant results on uploaded images
-  **Image Preview** - View uploaded images before and after prediction
-  **Responsive Design** - Works on desktop and mobile devices

## Prerequisites

- Python 3.8+
- Trained YOLOv5 model (`models/conv-model_V1.pt`)
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flask-app-brain-hemorrhage.git
   cd flask-app-brain-hemorrhage
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add trained model:**
   - Place your trained YOLOv5 model at `models/conv-model_V1.pt`
   - Create the `models/` directory if it doesn't exist
   - Model should be in PyTorch `.pt` format

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the app:**
   - Open your browser and navigate to `http://127.0.0.1:5000/`

## Usage

1. Click **"Choose..."** to select a medical image (PNG, JPG, JPEG)
2. The image preview will appear
3. Click **"Predict!"** to run the detection model
4. View results instantly

## Project Structure

```
flask-app-brain-hemorrhage/
├── app.py                 # Flask application main file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── models/
│   └── conv-model_V1.pt  # Trained YOLOv5 model (add if not present)
├── uploads/              # Temporary uploaded images
├── static/
│   ├── css/
│   │   └── main.css      # Styling
│   └── js/
│       └── main.js       # Client-side logic
└── templates/
    ├── base.html         # Base template
    └── index.html        # Main page template
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Display main interface |
| `/predict` | POST | Submit image and get prediction |

## Performance Notes

- Average prediction time: < 1 second
- Supports single image predictions
- Batch processing can be added for multiple images

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and research purposes. Medical diagnosis decisions should always be made by qualified healthcare professionals using proper diagnostic procedures.
