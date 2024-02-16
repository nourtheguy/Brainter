from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
import cv2
'''
def orb_sim(img1, img2):
    # Initialize ORB
    orb = cv2.ORB_create()
    # Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # Initialize matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors
    matches = bf.match(des1, des2)
    # Calculate similarity
    if len(matches) == 0:
        return 0
    similar_regions = [1 for m in matches if m.distance < 50]
    return len(similar_regions) / len(matches)
'''
def structural_sim(img1, img2):
    # Ensure images are the same size
    img2_resized = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
    data_range = 255

    # Calculate SSIM, specifying the data range for floating point images
    similarity, _ = ssim(img1, img2_resized, data_range=data_range, full=True)
    return similarity


original = cv2.imread('Image Similarity Score/img_1.png', 0) 
PCA_image = cv2.imread('Image Similarity Score/img_1_quantized_PCA.png', 0)
Kmeans_image = cv2.imread('Image Similarity Score/img_1_quantized.png', 0) 
'''
# Compare using ORB
orb_similarity1 = orb_sim(original, PCA_image)
orb_similarity2 = orb_sim(original, Kmeans_image)
'''
# Compare using SSIM
ssim_similarity1 = structural_sim(original, PCA_image)
ssim_similarity2 = structural_sim(original, Kmeans_image)
'''
print(f"ORB Similarity PCA: {orb_similarity1}")
print(f"ORB Similarity K Means: {orb_similarity2}")
print(f"SSIM Similarity PCA: {ssim_similarity1}")
print(f"SSIM Similarity K Means: {ssim_similarity2}")
'''
# Determine the most similar image based on ORB
''' if orb_similarity1 > orb_similarity2:
    print("PCA is more similar to the original image based on ORB.")
else:
    print("K Means is more similar to the original image based on ORB.")
'''

# Determine the most similar image based on SSIM
if ssim_similarity1 > ssim_similarity2:
    print("PCA is more similar to the original image based on SSIM.")
else:
    print("K Means is more similar to the original image based on SSIM.")
