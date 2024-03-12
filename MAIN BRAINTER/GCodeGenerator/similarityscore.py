from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
import cv2
import time


def structural_sim(img1, img2):
    # Ensure images are the same size
    img2_resized = resize(
        img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True
    )
    data_range = 255

    # Calculate SSIM, specifying the data range for floating point images
    similarity, _ = ssim(img1, img2_resized, data_range=data_range, full=True)
    return similarity
