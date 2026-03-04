# Models Directory

Place your trained YOLOv5 model file here.

## Expected Model File

- **Filename:** `conv-model_V1.pt`
- **Format:** PyTorch model file (`.pt`)
- **Model Type:** YOLOv5 custom trained model
- **Input:** Medical images (CT/MRI scans - any size supported)
- **Output:** Detection results with bounding boxes and confidence scores

## How to Add Your Model

1. Train your YOLOv5 model using your custom dataset:
   ```bash
   python train.py --img 640 --batch 16 --epochs 100 --data data.yaml --weights yolov5s.pt
   ```

2. Export or save your trained model as `.pt`:
   - The model is automatically saved in the `runs/detect/train/weights/` directory
   - Copy `best.pt` to this directory and rename to `conv-model_V1.pt`

3. Place the `.pt` file in this directory

## Model Training Format

If training with YOLOv5, ensure your dataset has:
- Proper COCO or YOLO format annotations
- Hemorrhage class labeled in your dataset
- Train/val/test splits configured

## Using Your .pt Model

1. Copy your trained `.pt` file here
2. Name it `conv-model_V1.pt`
3. Restart the Flask app
4. The model will be loaded automatically

## Model Requirements

- Must be YOLOv5 compatible format
- Should be trained on brain scan images
- Recommended input size: 640x640 (YOLOv5 default)
- Will auto-resize images during inference

## Note

The `.gitignore` file is configured to ignore `.pt` model files during git tracking.
Large model files should use Git LFS (Large File Storage) if version control is needed.

For more information, see [Setup Guide](../SETUP.md)
