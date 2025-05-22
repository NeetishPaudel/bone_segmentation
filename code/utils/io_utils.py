import SimpleITK as sitk
import nibabel as nib
import numpy as np

def read_image(filepath):
    image = sitk.ReadImage(filepath)
    nib_img = nib.load(filepath)
    affine = nib_img.affine
    return image, affine

def save_mask(mask_np, ref_img, filename):
    img = sitk.GetImageFromArray(mask_np)
    img.CopyInformation(ref_img)
    sitk.WriteImage(img, filename)
    print(f"Saved mask to {filename}")