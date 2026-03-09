# Camera Calibration Tool

This repository contains a Python-based camera calibration tool that uses OpenCV to calibrate cameras and correct lens distortion. The tool performs camera calibration using a chessboard pattern and provides functions for undistorting images.

## Features

- Camera calibration using chessboard patterns
- Extraction of camera matrix, distortion parameters, rotation vectors, and translation vectors
- Image undistortion with two methods: standard undistortion and remapping
- Reprojection error calculation to assess calibration quality
- Support for batch processing of calibration images

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Glob (for file searching)

See `requirements.txt` for the exact package versions.

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Prepare a set of calibration images containing a chessboard pattern (default: 9x6 inner corners)
2. Place the images in a directory (e.g., `calib_images/`)
3. Run the script:
   ```
   python camera_calib.py
   ```

The script will:
- Process all images matching the pattern `calib_images/*.jpeg`
- Detect chessboard corners in each image
- Calculate camera calibration parameters
- Save undistorted versions of the images
- Calculate and display the reprojection error

## Configuration

The calibration parameters can be adjusted in the `CameraCaliberation` class:

- `chessboard_size`: Number of inner corners per chessboard row and column (default: (9, 6))
- `frame_size`: Size of the images used for calibration (default: (1280, 720))
- `criteria`: Termination criteria for corner sub-pixel accuracy

## Classes and Methods

### CameraCaliberation

Main class for performing camera calibration:

- `caliberate(img_loc)`: Performs camera calibration using images from the specified location
- `undistort(cameraMatrix, distParam, img_dist, remap=False)`: Corrects distortion in a single image
- `reprojection_error(rvecs, tvecs, cameraMatrix, distParam)`: Calculates reprojection error

## Output

The script produces:
- Camera matrix and distortion parameters
- Undistorted images saved as `undistorted_image.jpg` or `undistorted_image_remap.jpg`
- Reprojection error metrics

## License

This project is licensed under the MIT License - see the LICENSE file for details.