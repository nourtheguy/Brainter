import cv2
import numpy as np


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


def apply_fixed_palette_color_reduction(image, colors):
    """
    Reduces the number of colors in an image using a fixed palette.

    :param image: The original image.
    :param colors: Array of RGB values of the predefined colors.
    :return: Image with reduced color palette.
    """
    # Create an empty array for the new image
    new_image = np.zeros_like(image)

    # Map each pixel to the closest color in the predefined set
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            new_image[i, j] = find_closest_color(image[i, j], colors)

    return new_image


def k_means_color_reduction(image_path, colors):
    """
    Reduces the number of colors in an image to the colors of a predefined palette.

    :param image_path: Path to the image file.
    :param colors: Array of RGB values of the predefined colors.
    :return: Image with reduced color palette.
    """

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Apply fixed palette color reduction
    reduced_image = apply_fixed_palette_color_reduction(image, colors)

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
        [255, 0, 0],  # Red
        [0, 255, 0],  # Green
        [0, 0, 255],  # Blue
        [0, 255, 255],  # Cyan
        [255, 0, 255],  # Magenta
        [255, 255, 0],  # Yellow
        [255, 165, 0],  # Orange
        [127, 255, 0],  # Chartreuse Green
        [0, 255, 127],  # Spring Green
        [0, 127, 255],  # Azure
        [127, 0, 255],  # Violet
        [255, 0, 127],  # Rose
    ]
)

# Example usage
if __name__ == "__main__":
    input_image_path = "img.png"
    output_image_path = "image_new.png"

    try:
        processed_image = k_means_color_reduction(input_image_path, preset_colors)
        save_image(processed_image, output_image_path)
        print("Image processed and saved successfully.")
    except Exception as e:
        print("Error:", e)
