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

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add trained model:**
   - Place your trained YOLOv5 model at `models/conv-model_V1.pt`
   - Create the `models/` directory if it doesn't exist
   - Model should be in PyTorch `.pt` format

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the app:**
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

## Technologies Used

- **Flask** - Web framework
- **PyTorch** - Deep learning library for model inference
- **YOLOv5** - Object detection model
- **OpenCV** - Image processing
- **Bootstrap 4** - UI framework
- **JavaScript** - Client-side interactions

## Model Details

- **Model Type:** Convolutional Neural Network (CNN) based on YOLOv5
- **Input Size:** 64x64 grayscale images
- **Output:** Classification prediction (hemorrhage detected/not detected)
- **Training Data:** Brain CT scans

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Display main interface |
| `/predict` | POST | Submit image and get prediction |

## Performance Notes

- Average prediction time: < 1 second
- Supports single image predictions
- Batch processing can be added for multiple images

## Known Limitations

- Currently processes one image at a time
- Requires high-resolution input images
- Model file must be in specific location

## Future Enhancements

- [ ] Batch image processing
- [ ] Result history/comparison
- [ ] Model accuracy metrics display
- [ ] Image preprocessing options
- [ ] Docker support
- [ ] API documentation (Swagger/OpenAPI)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and research purposes. Medical diagnosis decisions should always be made by qualified healthcare professionals using proper diagnostic procedures.