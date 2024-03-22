import cv2
import numpy as np
import time
from sklearn.cluster import KMeans


def color_quantization_kmeans(
    input_image_path,
    output_image_path,
    preset_colors,
    num_clusters=18,
    max_image_size=1024,
):
    """
    This function applies color quantization to an image using K-means clustering.
    It first reduces the number of colors to a specified number of clusters and then maps
    these colors to a set of preset colors. The quantized image is then saved to a file.

    Parameters:
    - input_image_path: Path to the input image file.
    - output_image_path: Path where the quantized image will be saved.
    - preset_colors: Array of RGB values representing the preset colors to map the image colors to.
    - num_clusters: The number of clusters to use for K-means clustering.
    - max_image_size: The maximum size (width or height) to which the image will be resized, to speed up processing.
    """

    def find_closest_color(pixel, colors):
        """
        Finds the closest color to a given pixel from a list of colors.

        Parameters:
        - pixel: The RGB values of the pixel.
        - colors: An array of RGB colors to find the closest color from.

        Returns:
        - The RGB values of the closest color found.
        """
        distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
        return colors[np.argmin(distances)]

    def k_means_cluster_colors(image, num_clusters):
        """
        Applies K-means clustering to reduce the number of colors in the image.

        Parameters:
        - image: The input image as a numpy array.
        - num_clusters: The number of clusters to use for the K-means algorithm.

        Returns:
        - An array of RGB values representing the centroids of the clusters.
        """
        pixels = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int)

    def map_clusters_to_preset(centroids, preset_colors):
        """
        Maps the cluster centroids to the closest preset color.

        Parameters:
        - centroids: The centroids of the clusters as RGB values.
        - preset_colors: The preset colors to map the centroids to.

        Returns:
        - An array of RGB values where each centroid is replaced by the closest preset color.
        """
        return np.array(
            [find_closest_color(centroid, preset_colors) for centroid in centroids]
        )

    def replace_colors(image, centroids, mapped_colors):
        """
        Replaces the colors in the original image with the mapped preset colors.

        Parameters:
        - image: The original image.
        - centroids: The centroids of the clusters.
        - mapped_colors: The preset colors mapped from the centroids.

        Returns:
        - The image with colors replaced by the closest mapped preset colors.
        """
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

# # Example usage
# if __name__ == "__main__":
#     input_image_path = "MAIN BRAINTER/GCodeGenerator/Assets/Images/test.png"
#     output_image_path = "MAIN BRAINTER/GCodeGenerator/Assets/Quantized Images/test_quantized.png"

#     try:
#         start_time = time.time()
#         color_quantization_kmeans(input_image_path, output_image_path, preset_colors)
#         end_time = time.time()
#         print(
#             f"Image processed and saved successfully. Time taken: {end_time - start_time:.2f} seconds."
#         )
#     except Exception as e:
#         print("Error:", e)
