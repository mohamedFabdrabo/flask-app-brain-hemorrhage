# Models Directory

Place your trained YOLOv5 model file here.

## Expected Model File

- **Filename:** `conv-model_V1.h5`
- **Format:** Keras/TensorFlow H5 format
- **Input:** 64x64 grayscale images
- **Output:** Binary classification (hemorrhage/no hemorrhage)

## How to Add Your Model

1. Train your YOLOv5 model using your dataset
2. Save the trained model: `model.save('conv-model_V1.h5')`
3. Place the `.h5` file in this directory

## Model Requirements

- Must be compatible with TensorFlow/Keras
- Should accept input shape: (64, 64, 1)
- Output should be a single value between 0 and 1
- Recommended to normalize input to [0, 1] range

## Note

The `.gitignore` file is configured to ignore `.h5` model files during git tracking.
If you want to version control your model (not recommended for large files), 
consider using Git LFS (Large File Storage).

For more information, see [Setup Guide](../SETUP.md)
