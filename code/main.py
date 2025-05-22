from config import INPUT_PATH, OUTPUT_FOLDER, THRESHOLD
from utils.io_utils import read_image, save_mask
from utils.processing_utils import segment_bones, expand_mask, randomized_expansion
from utils.mask_utils import dilate_masks, fill_holes_masks, dilate_and_resolve_overlap, combine_masks
import SimpleITK as sitk


def main():
    image, _ = read_image(INPUT_PATH)
    image_np = sitk.GetArrayFromImage(image)
    spacing = image.GetSpacing()[::-1]  # z,y,x

    femur_mask, tibia_mask = segment_bones(image_np, THRESHOLD)
    femur_dil, tibia_dil = dilate_masks(femur_mask, tibia_mask, 3)
    femur_filled, tibia_filled = fill_holes_masks(femur_dil, tibia_dil)
    femur_dil2, tibia_dil2 = dilate_and_resolve_overlap(femur_filled, tibia_filled, 5)

    combined_mask = combine_masks(femur_dil2, tibia_dil2)
    save_mask(combined_mask, image, OUTPUT_FOLDER + "tf_segmented.nii.gz")

    femur_exp_2mm = expand_mask(femur_dil2, spacing, 2.0)
    tibia_exp_2mm = expand_mask(tibia_dil2, spacing, 2.0)
    save_mask(combine_masks(femur_exp_2mm, tibia_exp_2mm), image, OUTPUT_FOLDER + "tf_expanded_2mm.nii.gz")

    femur_exp_4mm = expand_mask(femur_dil2, spacing, 4.0)
    tibia_exp_4mm = expand_mask(tibia_dil2, spacing, 4.0)
    save_mask(combine_masks(femur_exp_4mm, tibia_exp_4mm), image, OUTPUT_FOLDER + "tf_expanded_4mm.nii.gz")

    femur_rand_exp_2mm = randomized_expansion(femur_dil2, spacing, 2.0, 0.9)
    tibia_rand_exp_2mm = randomized_expansion(tibia_dil2, spacing, 2.0, 0.9)
    save_mask(combine_masks(femur_rand_exp_2mm, tibia_rand_exp_2mm), image, OUTPUT_FOLDER + "tf_random_expanded_2mm.nii.gz")

    femur_rand_exp_4mm = randomized_expansion(femur_dil2, spacing, 4.0, 0.9)
    tibia_rand_exp_4mm = randomized_expansion(tibia_dil2, spacing, 4.0, 0.9)
    save_mask(combine_masks(femur_rand_exp_4mm, tibia_rand_exp_4mm), image, OUTPUT_FOLDER + "tf_random_expanded_4mm.nii.gz")


if __name__ == "__main__":
    main()
