import cv2
import numpy as np


def vectorize_image(input_image_path, output_image_path):
    """
    Vectorizes the given image using contour detection.

    :param input_image_path: Path to the input image.
    :param output_image_path: Path where the vectorized image will be saved.
    """
    # Read the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Could not read the image.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding or edge detection
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty image to draw contours
    contour_image = np.zeros_like(image)

    # Draw contours
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)

    # Save or process the contours
    cv2.imwrite(output_image_path, contour_image)

    return contours  # Optionally return contours for further processing


# Example usage
if __name__ == "__main__":
    input_image_path = "path/to/input/image.png"
    output_image_path = "path/to/output/vectorized_image.png"

    try:
        contours = vectorize_image(input_image_path, output_image_path)
        print("Image vectorization completed successfully.")
    except Exception as e:
        print("Error:", e)
