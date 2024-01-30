import cv2
import numpy as np
import time
from sklearn.cluster import KMeans


def quantize_image_colors(
    input_image_path,
    output_image_path,
    preset_colors,
    num_clusters=18,
    max_image_size=1024,
):
    """
    Function to apply color quantization to an image.

    :param input_image_path: Path to the input image.
    :param output_image_path: Path where the quantized image will be saved.
    :param preset_colors: Array of RGB values of the preset colors.
    :param num_clusters: Number of clusters for K-means.
    :param max_image_size: Maximum size to which the image is resized.
    """

    def find_closest_color(pixel, colors):
        distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
        return colors[np.argmin(distances)]

    def k_means_cluster_colors(image, num_clusters):
        pixels = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int)

    def map_clusters_to_preset(centroids, preset_colors):
        return np.array(
            [find_closest_color(centroid, preset_colors) for centroid in centroids]
        )

    def replace_colors(image, centroids, mapped_colors):
        new_image = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                original_color = image[i, j]
                closest_centroid = find_closest_color(original_color, centroids)
                new_color = find_closest_color(closest_centroid, mapped_colors)
                new_image[i, j] = new_color
        return new_image

    # Read the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Resize if necessary
    height, width = image.shape[:2]
    if max(height, width) > max_image_size:
        scaling_factor = max_image_size / max(height, width)
        image = cv2.resize(
            image,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv2.INTER_AREA,
        )

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Quantization process
    centroids = k_means_cluster_colors(image, num_clusters)
    mapped_colors = map_clusters_to_preset(centroids, preset_colors)
    reduced_image = replace_colors(image, centroids, mapped_colors)

    # Convert back to BGR for saving
    reduced_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2BGR)

    # Save the image
    cv2.imwrite(output_image_path, reduced_image)


# Preset List of colors
preset_colors = np.array(
    [
        [0, 0, 0],  # Black
        [135, 135, 135],  # Grey
        [180, 20, 20],  # Red
        [50, 160, 50],  # Green
        [50, 50, 180],  # Blue
        [60, 224, 224],  # Cyan
        [125, 47, 228],  # Purple
        [218, 218, 40],  # Yellow
        [255, 137, 38],  # Orange
        [243, 243, 243],  # Light Grey
        [24, 69, 77],  # Teal
        [0, 127, 255],  # Azure
        [170, 90, 150],  # Pink
    ]
)

# Example usage
if __name__ == "__main__":
    input_image_path = "G-Code Generator/Assets/Images/img_1.png"
    output_image_path = "G-Code Generator/Assets/Quantized Images/img_1_quantized.png"

    try:
        start_time = time.time()
        quantize_image_colors(input_image_path, output_image_path, preset_colors)
        end_time = time.time()
        print(
            f"Image processed and saved successfully. Time taken: {end_time - start_time:.2f} seconds."
        )
    except Exception as e:
        print("Error:", e)
