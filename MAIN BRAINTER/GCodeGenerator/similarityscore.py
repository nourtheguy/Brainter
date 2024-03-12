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
    start_time = time.time()  # Start timing
    similarity, _ = ssim(img1, img2_resized, data_range=data_range, full=True)
    end_time = time.time()  # End timing
    duration = end_time - start_time  # Calculate duration
    print(f"SSIM calculation took {duration} seconds.")
    return similarity


original = cv2.imread("Image Similarity Score/img_1.png", 0)
PCA_image = cv2.imread("Image Similarity Score/img_1_quantized_PCA.png", 0)
Kmeans_image = cv2.imread("Image Similarity Score/img_1_quantized.png", 0)

ssim_similarity1 = structural_sim(original, PCA_image)
ssim_similarity2 = structural_sim(original, Kmeans_image)

if ssim_similarity1 > ssim_similarity2:
    print("PCA is more similar to the original image based on SSIM.")
else:
    print("K Means is more similar to the original image based on SSIM.")
