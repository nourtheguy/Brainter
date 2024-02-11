import cv2
import numpy as np
import time
from sklearn.decomposition import PCA


# Define the color quantization function
def color_quantization(
    input_image_path,
    output_image_path,
    preset_colors,
    num_components=3,
    max_image_size=1024,
):
    """
    Applies color quantization to an image using PCA and maps the reduced colors to preset colors.

    Parameters:
    - input_image_path: Path to the input image file.
    - output_image_path: Path where the quantized image will be saved.
    - preset_colors: Array containing RGB values of the colors to map the image colors to.
    - num_components: Number of principal components to keep in PCA.
    - max_image_size: Maximum size (height or width) to which the image is resized to reduce processing time.
    """

    # Function to find the closest color in the preset colors to a given pixel
    def find_closest_color(pixel, colors):
        distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
        return colors[np.argmin(distances)]

    # Function to reduce the number of colors in the image using PCA
    def pca_reduce_colors(image, num_components):
        pixels = image.reshape((-1, 3))  # Reshape image to a 2D array of pixels
        pca = PCA(n_components=num_components)  # Initialize PCA
        reduced_colors = pca.fit_transform(
            pixels
        )  # Reduce the dimensionality of the pixel colors
        reconstructed_pixels = pca.inverse_transform(
            reduced_colors
        )  # Reconstruct pixel colors from the reduced dimensions
        reconstructed_pixels = np.clip(reconstructed_pixels, 0, 255).astype(
            np.uint8
        )  # Clip values to valid range
        return reconstructed_pixels.reshape(
            image.shape
        )  # Reshape back to the original image shape

    # Function to map the reduced colors to the preset colors
    def map_colors_to_preset(image, preset_colors):
        mapped_image = np.zeros_like(image)  # Initialize the mapped image array
        for i in range(image.shape[0]):  # Iterate over image rows
            for j in range(image.shape[1]):  # Iterate over image columns
                original_color = image[i, j]  # Get the original color of the pixel
                new_color = find_closest_color(
                    original_color, preset_colors
                )  # Find the closest preset color
                mapped_image[i, j] = new_color  # Set the pixel to the new color
        return mapped_image

    # Read the image from the input path
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Resize the image if it's larger than the maximum size
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

    # Convert the image from BGR (OpenCV default) to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Apply PCA to reduce the colors in the image
    reduced_image = pca_reduce_colors(image, num_components)

    # Map the reduced colors to the preset colors
    quantized_image = map_colors_to_preset(reduced_image, preset_colors)

    # Convert the quantized image back to BGR color space for saving
    quantized_image = cv2.cvtColor(quantized_image, cv2.COLOR_RGB2BGR)

    # Save the quantized image to the specified output path
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
    input_image_path = "G-Code Generator/Assets/Images/test.png"
    output_image_path = (
        "G-Code Generator/Assets/Quantized Images/test_quantized_PCA.png"
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
