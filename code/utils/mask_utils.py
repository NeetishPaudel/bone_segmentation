import numpy as np
from scipy.ndimage import binary_fill_holes, binary_dilation

def fill_holes_2d_all_axes(mask_3d):
    def fill_along_axis(arr, axis):
        filled = np.zeros_like(arr)
        for i in range(arr.shape[axis]):
            if axis == 0:
                filled[i] = binary_fill_holes(arr[i])
            elif axis == 1:
                filled[:, i] = binary_fill_holes(arr[:, i])
            elif axis == 2:
                filled[:, :, i] = binary_fill_holes(arr[:, :, i])
        return filled.astype(np.uint8)

    return fill_along_axis(fill_along_axis(fill_along_axis(mask_3d, 0), 1), 2)

def dilate_masks(femur_mask, tibia_mask, structure_size):
    structure = np.ones((structure_size,) * 3)
    femur_dilated = binary_dilation(femur_mask, structure=structure)
    tibia_dilated = binary_dilation(tibia_mask, structure=structure)
    return femur_dilated, tibia_dilated

def fill_holes_masks(femur_mask, tibia_mask):
    femur_filled = fill_holes_2d_all_axes(femur_mask)
    tibia_filled = fill_holes_2d_all_axes(tibia_mask)
    femur_filled = fill_holes_2d_all_axes(femur_filled)
    tibia_filled = fill_holes_2d_all_axes(tibia_filled)
    femur_filled = binary_fill_holes(femur_filled).astype(np.uint8)
    tibia_filled = binary_fill_holes(tibia_filled).astype(np.uint8)
    return femur_filled, tibia_filled

def dilate_and_resolve_overlap(femur_mask, tibia_mask, structure_size):
    structure = np.ones((structure_size,) * 3)
    femur_dilated = binary_dilation(femur_mask, structure=structure)
    tibia_dilated = binary_dilation(tibia_mask, structure=structure)
    overlap = femur_dilated & tibia_dilated
    femur_dilated[overlap] = 0
    tibia_dilated[overlap] = 0
    return femur_dilated, tibia_dilated

def combine_masks(femur_mask, tibia_mask):
    combined = np.zeros_like(femur_mask, dtype=np.uint8)
    combined[femur_mask == 1] = 1
    combined[tibia_mask == 1] = 2
    return combined