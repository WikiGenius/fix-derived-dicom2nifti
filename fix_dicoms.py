# Import Important libraries
import os
import pydicom
import glob
import pathlib
import cv2
import numpy as np
from skimage.exposure import rescale_intensity
import config

# loop over original patients
for patient in os.listdir(config.original_patients):
    orig_patient_path = os.path.join(config.original_patients, patient)
    # Create correct_patient_path sub directory
    correct_patient_path = os.path.join(config.correct_patients, patient)
    pathlib.Path(f'{correct_patient_path}').mkdir(
        parents=True, exist_ok=True)
    # dicom files paths in single patient
    dicom_files = glob.glob(orig_patient_path+'/*')

    # some lists for sorting dicom with slicing order to keep every thing order
    instance_number = []
    ds_list = []
    # Loop over dicom files to sort their orders with the order of the slices
    for i, dicom_file in enumerate(dicom_files):
        ds = pydicom.read_file(dicom_file)
        ds_list.append(ds)
        instance_number.append(int(ds.InstanceNumber))

    s_instance_number, s_dicom_files, s_ds_list = zip(
        *sorted(zip(instance_number, dicom_files,  ds_list)))

    # Initial pos from the initial position
    pos = config.pos0.copy()

    # Loop over dicom files with respect to InstanceNumber
    for i, dicom_file in enumerate(s_dicom_files):
        # Exclude any dicom has not global shape with rows = 512
        if s_ds_list[i].pixel_array.shape[0] != 512:
            continue

        ds = s_ds_list[i]
        # check whether thes important attributes exist or not to fix converting
        if 'ImagePositionPatient' not in ds:
            ds.ImagePositionPatient = pos
        if 'ImageOrientationPatient' not in ds:
            ds.ImageOrientationPatient = config.theta
        if 'PixelSpacing' not in ds:
            ds.PixelSpacing = config.p_spacing
        # check if they are MONOCHROME2 or RGB
        if not ds.PhotometricInterpretation == 'MONOCHROME2':
            img = ds.pixel_array  # dtype = uint8 RGB
            # convert images to gray
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.asarray(img)
            # To avoid any overflow
            img = img.astype(float)
            # rescale intensity to have 2 bytes = 2^16 bits
            img = rescale_intensity(1.0*img, in_range=(0, 255))
            # 2^12 - 1 = 4095
            img = (img * 4095).astype("uint16")
            img = cv2.GaussianBlur(img, config.K_GUASSIAN, 0)
            # modify DICOM tags
            ds.PhotometricInterpretation = 'MONOCHROME2'
            ds.SamplesPerPixel = 1
            ds.BitsAllocated = 16
            ds.BitsStored = 12
            ds.HighBit = 11
            ds.is_little_endian = True
            ds.fix_meta_info()

            # save pixel data and dicom file
            ds.PixelData = img.tobytes()
        ds.save_as(os.path.join(correct_patient_path,
                   dicom_file.split('/')[-1]))
        pos[2] += 1.5
    pos = config.pos0.copy()

print('all patients now are valid for converting to nifti in correct_patients directory')
