import cv2
import numpy as np
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


def color_reduction_with_kmeans(image_path, preset_colors, num_clusters=100):
    """
    Apply color reduction using K-means clustering and a preset color palette.

    :param image_path: Path to the image file.
    :param preset_colors: Preset array of colors.
    :param num_clusters: Number of clusters for K-means.
    :return: Image with reduced color palette.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Apply K-means clustering
    centroids = k_means_cluster_colors(image, num_clusters)

    # Map centroids to preset colors
    mapped_colors = map_clusters_to_preset(centroids, preset_colors)

    # Replace colors in the image
    reduced_image = replace_colors(image, centroids, mapped_colors)

    return reduced_image


def save_image(image, output_path):
    """
    Saves the processed image to a file.

    :param image: The processed image.
    :param output_path: Path for saving the image.
    """
    cv2.imwrite(output_path, image)


# Define your 12 preset colors (example RGB values)
preset_colors = np.array(
    [
        [0, 0, 0],  # Black
        [232, 238, 251],  # Grey
        [255, 0, 0],  # Red
        [0, 128, 0],  # Green (Darker Shade)
        [0, 0, 255],  # Blue
        [0, 255, 255],  # Cyan
        [255, 0, 255],  # Magenta
        [255, 255, 0],  # Yellow
        [255, 165, 0],  # Orange
        [128, 128, 0],  # Olive Green
        [0, 128, 128],  # Teal
        [0, 127, 255],  # Azure
        [128, 0, 0],  # Maroon
    ]
)

# Example usage
if __name__ == "__main__":
    input_image_path = "G-Code Generator/Assets/img_4.png"
    output_image_path = "G-Code Generator/Assets/img_3_quantized.png"

    try:
        processed_image = color_reduction_with_kmeans(input_image_path, preset_colors)
        save_image(processed_image, output_image_path)
        print("Image processed and saved successfully.")
    except Exception as e:
        print("Error:", e)
