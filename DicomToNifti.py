import dicom2nifti
import os
import pathlib

import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()


path_patients = "correct_patients"
path_out_data = "PhD_Pictures"
# Create patient_path_nifti sub directory
pathlib.Path(f'{path_out_data}').mkdir(parents=True, exist_ok=True)

for i, patient in enumerate(os.listdir(path_patients)):
    patient_path_dicoms = os.path.join(path_patients, patient)
    patient_path_nifti = os.path.join(path_out_data, patient)
    nifti_file = patient_path_nifti+'.nii.gz'
    dicom2nifti.dicom_series_to_nifti(patient_path_dicoms, nifti_file)

print('finish converting')