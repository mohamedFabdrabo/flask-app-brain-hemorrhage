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
import traceback

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
    # Try loading with torch.jit or direct torch.load first
    if MODEL_PATH.endswith('.pt'):
        try:
            # Direct PyTorch model loading
            model = torch.load(MODEL_PATH, map_location=device)
            if hasattr(model, 'eval'):
                model.eval()
            print(f'✓ Model loaded successfully from {MODEL_PATH}')
            print('✓ Server running at http://127.0.0.1:5000/')
        except Exception as e:
            # Fallback to torch.hub if direct loading fails
            print(f'Attempting to load via torch.hub (this may take a moment)...')
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=False)
            model.to(device)
            model.eval()
            print(f'✓ Model loaded successfully from {MODEL_PATH}')
            print('✓ Server running at http://127.0.0.1:5000/')
    else:
        print(f'✗ Error: Model file must be .pt format')
        model = None
except FileNotFoundError:
    print(f'✗ Error: Model file not found at {MODEL_PATH}')
    print('  Please ensure the model file exists in the models/ directory')
    model = None
except Exception as e:
    print(f'✗ Error loading model: {str(e)}')
    print(f'  Type: {type(e).__name__}')
    print('  Make sure you have:')
    print('  1. The correct .pt model file in models/ directory')
    print('  2. PyTorch properly installed')
    print('  3. Internet connection (for torch.hub fallback)')
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
        if model is None:
            return {'error': 'Model not loaded. Check server logs.', 'success': False}
        
        # Read image
        print(f'Reading image from: {img_path}')
        img = cv2.imread(img_path)
        
        if img is None:
            print(f'ERROR: Failed to read image: {img_path}')
            return {'error': 'Failed to load image', 'success': False}
        
        print(f'Image shape: {img.shape}')
        
        # Run inference
        print('Starting model inference...')
        with torch.no_grad():
            try:
                # Try YOLOv5 style inference
                print(f'Model type: {type(model)}')
                results = model(img)
                print(f'Inference complete. Results type: {type(results)}')
                
                # Check if results has expected YOLOv5 format
                if hasattr(results, 'xyxy'):
                    print(f'Results has xyxy attribute. Number of detections: {len(results.xyxy[0])}')
                    # YOLOv5 detection results
                    detections = results.xyxy[0].cpu().numpy() if len(results.xyxy[0]) > 0 else []
                    
                    if len(detections) > 0:
                        max_confidence = float(np.max(detections[:, 4])) * 100
                        prediction_text = 'Hemorrhage Detected'
                        confidence = round(max_confidence, 2)
                        print(f'Detected hemorrhage with confidence: {confidence}%')
                    else:
                        prediction_text = 'No Hemorrhage Detected'
                        confidence = 0.0
                        print('No hemorrhage detected')
                else:
                    # Fallback for other model types
                    print(f'WARNING: Results does not have xyxy attribute. Available attributes: {dir(results)}')
                    prediction_text = f'Model output: {type(results)}'
                    confidence = 0.0
                    detections = []
                
                return {
                    'success': True,
                    'confidence': confidence,
                    'prediction': prediction_text,
                    'detections': int(len(detections)) if len(detections) > 0 else 0
                }
            except AttributeError as ae:
                print(f'ERROR: AttributeError during inference: {str(ae)}')
                print(f'Traceback: {traceback.format_exc()}')
                return {
                    'error': f'Model format error: {str(ae)}. Ensure model is in YOLOv5 format.',
                    'success': False
                }
    
    except Exception as e:
        print(f'ERROR in model_predict: {str(e)}')
        print(f'Traceback: {traceback.format_exc()}')
        return {'error': f'Prediction error: {str(e)}', 'success': False}


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
                print('ERROR: Model not loaded')
                return jsonify({'error': 'Model not loaded', 'success': False}), 500
            
            # Check if file is in request
            if 'file' not in request.files:
                print('ERROR: No file in request')
                return jsonify({'error': 'No file provided', 'success': False}), 400
            
            file = request.files['file']
            
            # Validate file
            if file.filename == '':
                print('ERROR: No file selected')
                return jsonify({'error': 'No file selected', 'success': False}), 400
            
            if not allowed_file(file.filename):
                print(f'ERROR: Invalid file type: {file.filename}')
                return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG', 'success': False}), 400
            
            # Save file securely
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f'Saving file to: {filepath}')
            file.save(filepath)
            
            # Make prediction
            print(f'Running prediction on: {filepath}')
            result = model_predict(filepath)
            print(f'Prediction result: {result}')
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
                print(f'Cleaned up file: {filepath}')
            except Exception as cleanup_err:
                print(f'Warning: Could not delete file: {cleanup_err}')
            
            if not result.get('success'):
                print(f'Prediction failed: {result}')
                return jsonify(result), 400
            
            print(f'Prediction successful: {result}')
            return jsonify(result), 200
        
        except Exception as e:
            error_msg = f'Prediction failed: {str(e)}'
            print(f'EXCEPTION: {error_msg}')
            print(f'Traceback: {traceback.format_exc()}')
            return jsonify({'error': error_msg, 'success': False}), 500
    
    return jsonify({'error': 'Method not allowed', 'success': False}), 405


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

