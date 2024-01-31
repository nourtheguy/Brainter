import cv2
import numpy as np
import os


def color_segmentation(input_image_path, output_folder, preset_colors, color_names):
    """
    Segment each color in the image and save grayscale representations only for colors present in the image.

    :param input_image_path: Path to the quantized image.
    :param output_folder: Folder to save the output images.
    :param preset_colors: Preset array of colors.
    :param color_names: List of names corresponding to each color in the preset.
    """

    def segment_color(image, color):
        mask = cv2.inRange(image, color, color)
        if np.any(mask):  # Check if the color is present in the image
            grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            # If the color is black, invert the grayscale image to make the mask visible
            if np.all(color == [0, 0, 0]):
                grayscale = 255 - grayscale  # Invert grayscale
            return cv2.bitwise_and(grayscale, grayscale, mask=mask)
        else:
            return None

    # Read the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each color and save the file only if the color is present
    for color, name in zip(preset_colors, color_names):
        segmented_image = segment_color(image, color)
        if segmented_image is not None:  # Only save if the color is present
            output_path = os.path.join(output_folder, f"{name}.png")
            cv2.imwrite(output_path, segmented_image)


# Preset List of colors from color_quantization.py
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

color_names = [
    "Black",
    "Grey",
    "Red",
    "Green",
    "Blue",
    "Cyan",
    "Purple",
    "Yellow",
    "Orange",
    "Light Grey",
    "Teal",
    "Azure",
    "Pink",
]


# Example usage
if __name__ == "__main__":
    input_image_path = "G-Code Generator/Assets/Quantized Images/test_quantized.png"
    output_folder = "G-Code Generator/Assets/Segmented Images/test"

    try:
        color_segmentation(input_image_path, output_folder, preset_colors, color_names)
        print("Color segmentation completed successfully.")
    except Exception as e:
        print("Error:", e)
