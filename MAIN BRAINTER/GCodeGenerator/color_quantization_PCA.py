import cv2
import numpy as np
import time
from sklearn.decomposition import PCA


def color_quantization(
    input_image_path,
    output_image_path,
    preset_colors,
    num_components=3,
    max_image_size=1024,
):
    """
    Function to apply color quantization to an image using PCA.

    :param input_image_path: Path to the input image.
    :param output_image_path: Path where the quantized image will be saved.
    :param preset_colors: Array of RGB values of the preset colors.
    :param num_components: Number of principal components to keep.
    :param max_image_size: Maximum size to which the image is resized.
    """

    def find_closest_color(pixel, colors):
        distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
        return colors[np.argmin(distances)]

    def pca_reduce_colors(image, num_components):
        pixels = image.reshape((-1, 3))
        pca = PCA(n_components=num_components)
        reduced_colors = pca.fit_transform(pixels)
        reconstructed_pixels = pca.inverse_transform(reduced_colors)
        # Ensure the reconstructed pixels are clipped to valid range and converted to uint8
        reconstructed_pixels = np.clip(reconstructed_pixels, 0, 255).astype(np.uint8)
        return reconstructed_pixels.reshape(image.shape)

    def map_colors_to_preset(image, preset_colors):
        mapped_image = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                original_color = image[i, j]
                new_color = find_closest_color(original_color, preset_colors)
                mapped_image[i, j] = new_color
        return mapped_image

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

    # PCA color reduction
    reduced_image = pca_reduce_colors(image, num_components)

    # Map reduced colors to preset colors
    quantized_image = map_colors_to_preset(reduced_image, preset_colors)

    # Convert back to BGR for saving
    quantized_image = cv2.cvtColor(quantized_image, cv2.COLOR_RGB2BGR)

    # Save the image
    cv2.imwrite(output_image_path, quantized_image)


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
    input_image_path = "GCodeGenerator/Assets/Images/img_5.png"
    output_image_path = (
        "GCodeGenerator/Assets/Quantized Images/img_5_quantized_PCA.png"
    )

    try:
        start_time = time.time()
        color_quantization(input_image_path, output_image_path, preset_colors)
        end_time = time.time()
        print(
            f"Image processed and saved successfully. Time taken: {end_time - start_time:.2f} seconds."
        )
    except Exception as e:
        print("Error:", e)
