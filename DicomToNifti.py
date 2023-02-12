import dicom2nifti
import os
import pathlib

import dicom2nifti.settings as settings
import config

settings.disable_validate_slice_increment()

# Create patient_path_nifti sub directory
pathlib.Path(f'{config.path_out_data_nifti}').mkdir(parents=True, exist_ok=True)

for i, patient in enumerate(os.listdir(config.correct_patients)):
    patient_path_dicoms = os.path.join(config.correct_patients, patient)
    patient_path_nifti = os.path.join(config.path_out_data_nifti, patient)
    nifti_file = patient_path_nifti+'.nii.gz'
    dicom2nifti.dicom_series_to_nifti(patient_path_dicoms, nifti_file)

print('finish converting')