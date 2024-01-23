import cv2
import numpy as np
import time
from sklearn.cluster import KMeans


def find_closest_color(pixel, colors):
    """
    Find the closest color to the given pixel from the predefined set.

    :param pixel: The RGB values of the pixel.
    :param colors: Array of RGB values of the predefined colors.
    :return: RGB values of the closest color.
    """
    distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
    index_of_smallest = np.argmin(distances)
    return colors[index_of_smallest]


def k_means_cluster_colors(image, num_clusters):
    """
    Apply K-means clustering to the image to find main colors.

    :param image: The original image.
    :param num_clusters: Number of clusters to use in K-means.
    :return: Array of centroid colors from K-means clustering.
    """
    # Reshape the image to be a list of pixels
    pixels = image.reshape((-1, 3))

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)
    centroids = kmeans.cluster_centers_.astype(int)

    return centroids


def map_clusters_to_preset(centroids, preset_colors):
    """
    Map the centroids to the closest colors from the preset colors.

    :param centroids: Centroids from K-means clustering.
    :param preset_colors: Preset array of colors.
    :return: Mapped colors.
    """
    mapped_colors = np.array(
        [find_closest_color(centroid, preset_colors) for centroid in centroids]
    )
    return mapped_colors


def replace_colors(image, centroids, mapped_colors):
    """
    Replace colors in the image based on the mapped colors.

    :param image: Original image.
    :param centroids: Centroids from K-means clustering.
    :param mapped_colors: Colors mapped to the preset.
    :return: Image with colors replaced.
    """
    new_image = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            original_color = image[i, j]
            closest_centroid = find_closest_color(original_color, centroids)
            new_color = find_closest_color(closest_centroid, mapped_colors)
            new_image[i, j] = new_color

    return new_image


def color_reduction_with_kmeans(
    image_path, preset_colors, num_clusters=18, max_image_size=1024
):
    """
    Apply color reduction using K-means clustering and a preset color palette.

    :param image_path: Path to the image file.
    :param preset_colors: Preset array of colors.
    :param num_clusters: Number of clusters for K-means.
    :param max_image_size: Maximum size to which the image is resized.
    :return: Image with reduced color palette.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Resize if the image is too large
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

    # Apply K-means clustering
    centroids = k_means_cluster_colors(image, num_clusters)

    # Map centroids to preset colors
    mapped_colors = map_clusters_to_preset(centroids, preset_colors)

    # Replace colors in the image
    reduced_image = replace_colors(image, centroids, mapped_colors)

    # Convert back to BGR for saving
    reduced_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2BGR)

    return reduced_image


def save_image(image, output_path):
    """
    Saves the processed image to a file.

    :param image: The processed image.
    :param output_path: Path for saving the image.
    """
    cv2.imwrite(output_path, image)


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
    input_image_path = "G-Code Generator/Assets/img_4.png"
    output_image_path = "G-Code Generator/Assets/img_4_quantized.png"

    try:
        start_time = time.time()  # Starting the timer

        processed_image = color_reduction_with_kmeans(input_image_path, preset_colors)
        save_image(processed_image, output_image_path)

        end_time = time.time()  # Ending the timer
        duration = end_time - start_time  # Calculating the duration of the process

        print(
            f"Image processed and saved successfully. Time taken: {duration:.2f} seconds."
        )

    except Exception as e:
        print("Error:", e)
