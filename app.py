from __future__ import division, print_function
# coding=utf-8
"""
Brain Hemorrhage Detection Flask Application
Uses a trained YOLOv5 model for image classification
"""
import sys
import os
import glob
import re
import numpy as np
import cv2
import torch

# PyTorch model loading

# Flask utilities
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Initialize Flask app
app = Flask(__name__)

# Configuration
MODEL_PATH = 'models/conv-model_V1.pt'  # YOLOv5 PyTorch model
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Set device (GPU if available, else CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Load trained model
model = None
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=False)
    model.to(device)
    model.eval()
    print(f'✓ Model loaded successfully from {MODEL_PATH}')
    print('✓ Server running at http://127.0.0.1:5000/')
except FileNotFoundError:
    print(f'✗ Error: Model file not found at {MODEL_PATH}')
    print('  Please ensure the model file exists in the models/ directory')
    model = None
except Exception as e:
    print(f'✗ Error loading model: {str(e)}')
    print('  Make sure you have the correct .pt model file')
    model = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def model_predict(img_path):
    """
    Predict brain hemorrhage presence in medical image using YOLOv5
    
    Args:
        img_path (str): Path to the input image
        
    Returns:
        dict: Prediction results with confidence scores
    """
    try:
        # Read image
        img = cv2.imread(img_path)
        
        if img is None:
            return {'error': 'Failed to load image', 'success': False}
        
        # Run YOLOv5 inference
        with torch.no_grad():
            results = model(img)
        
        # Process results
        detections = results.xyxy[0].cpu().numpy() if len(results.xyxy[0]) > 0 else []
        
        if len(detections) > 0:
            # Found hemorrhage(s)
            max_confidence = float(np.max(detections[:, 4])) * 100  # Confidence score
            prediction_text = 'Hemorrhage Detected'
            confidence = round(max_confidence, 2)
        else:
            # No hemorrhage detected
            prediction_text = 'No Hemorrhage Detected'
            confidence = 0.0
        
        return {
            'success': True,
            'confidence': confidence,
            'prediction': prediction_text,
            'detections': int(len(detections))
        }
    
    except Exception as e:
        return {'error': str(e), 'success': False}


@app.route('/', methods=['GET'])
def index():
    """
    Render main interface page
    """
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Handle image upload and prediction
    
    POST: Upload image and get prediction
    Returns:
        JSON: Prediction results or error message
    """
    if request.method == 'POST':
        try:
            # Check if model is loaded
            if model is None:
                return jsonify({'error': 'Model not loaded', 'success': False}), 500
            
            # Check if file is in request
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided', 'success': False}), 400
            
            file = request.files['file']
            
            # Validate file
            if file.filename == '':
                return jsonify({'error': 'No file selected', 'success': False}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG', 'success': False}), 400
            
            # Save file securely
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Make prediction
            result = model_predict(filepath)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            if not result.get('success'):
                return jsonify(result), 400
            
            return jsonify(result), 200
        
        except Exception as e:
            return jsonify({'error': f'Prediction failed: {str(e)}', 'success': False}), 500
    
    return jsonify({'error': 'Method not allowed', 'success': False}), 405


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

