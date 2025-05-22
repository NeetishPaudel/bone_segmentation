import numpy as np
from scipy.ndimage import label, distance_transform_edt
from skimage.measure import marching_cubes
from .mask_utils import fill_holes_2d_all_axes

def segment_bones(image_array, threshold):
    bone_mask = image_array > threshold
    labeled_array, num_features = label(bone_mask)
    print(f"Number of components found: {num_features}")

    sizes = [(labeled_array == i).sum() for i in range(1, num_features + 1)]
    top2 = sorted(range(len(sizes)), key=lambda i: sizes[i], reverse=True)[:2]
    femur_label = top2[0] + 1
    tibia_label = top2[1] + 1

    femur_mask = (labeled_array == femur_label).astype(np.uint8)
    tibia_mask = (labeled_array == tibia_label).astype(np.uint8)
    return femur_mask, tibia_mask

def expand_mask(mask_np, spacing, expansion_mm):
    distance = distance_transform_edt(1 - mask_np, sampling=spacing)
    expanded = (distance <= expansion_mm).astype(np.uint8)
    return expanded

def randomized_expansion(mask_np, voxel_spacing, max_expansion_mm=2.0, random_factor=0.5):
    from scipy.ndimage import binary_dilation
    import SimpleITK as sitk
    expansion_voxels = [max_expansion_mm / s for s in voxel_spacing]
    max_radius = max(expansion_voxels)

    grid = np.linspace(-max_radius, max_radius, int(max_radius * 2) + 1)
    x, y, z = np.meshgrid(grid, grid, grid)
    kernel = (x ** 2 / expansion_voxels[0] ** 2 + y ** 2 / expansion_voxels[1] ** 2 + z ** 2 / expansion_voxels[2] ** 2 <= 1).astype(np.uint8)

    expanded_mask = binary_dilation(mask_np, structure=kernel).astype(np.uint8)
    boundary = expanded_mask - mask_np

    sitk_img = sitk.GetImageFromArray(mask_np.astype(np.uint8))
    sitk_img.SetSpacing(voxel_spacing)
    distance_map = sitk.SignedMaurerDistanceMap(sitk_img, squaredDistance=False, useImageSpacing=True)
    dist_array = sitk.GetArrayFromImage(distance_map)

    randomized_mask = mask_np.copy()
    b_coords = np.where(boundary == 1)
    for x_, y_, z_ in zip(*b_coords):
        dist = dist_array[x_, y_, z_]
        if dist <= max_expansion_mm:
            thresh = np.random.uniform(0, max_expansion_mm * random_factor)
            if dist <= thresh:
                randomized_mask[x_, y_, z_] = 1

    randomized_mask = np.maximum(randomized_mask, mask_np)
    randomized_mask = np.minimum(randomized_mask, expanded_mask)
    return randomized_mask