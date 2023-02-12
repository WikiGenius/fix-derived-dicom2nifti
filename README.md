# DICOM to NIFTI conversion code

This code is used for converting DICOM files to NIFTI format.

## Requirements
* Python 3
* pydicom
* OpenCV
* NumPy
* Scikit-image

## How to use
1. Install the required packages by running `pip install -r requirements.txt`
2. Update the `config.py` file with the required information, such as the directory path where the original patients are stored, the directory path where the corrected patients will be stored, and the initial position and orientation of the images.
3. Run the script using `python dicom_to_nifti.py`

## What the code does
1. Imports necessary libraries.
2. Loops over the original patients directory to process each patient.
3. Sorts the DICOM files for each patient based on the instance number to ensure that the slices are in the correct order.
4. Corrects important attributes in the DICOM files, such as ImagePositionPatient, ImageOrientationPatient, and PixelSpacing, if they do not exist.
5. Converts the images from RGB to grayscale, rescales the intensity, applies Gaussian blur, and modifies the DICOM tags.
6. Saves the corrected DICOM files in the correct patients directory.
7. Finally, all patients have been converted to valid NIFTI format and are stored in the correct patients directory.

