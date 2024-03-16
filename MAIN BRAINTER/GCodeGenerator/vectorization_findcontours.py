from PIL import Image
import svgwrite
import numpy as np
import cv2
import os


def vectorization(input_folder, output_folder):
    """
    Process all images in the specified input folder, converting them to SVG format with shape fills
    using contour detection, and save the results in the output folder.

    Parameters:
    - input_folder: Path to the folder containing the input images.
    - output_folder: Path to the folder where the SVG files will be saved.
    """

    def process_image(image_path, svg_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Get the dimensions of the input image to size the background rectangle
        height, width = img.shape[:2]

        dwg = svgwrite.Drawing(svg_path, profile="tiny", size=(width, height))

        # Add a black background rectangle
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="black"))

        for contour in contours:
            # Convert each point in the contour to a tuple (x, y)
            points = [(int(point[0][0]), int(point[0][1])) for point in contour]
            # Add a polygon for each contour using the points, filled with white
            dwg.add(dwg.polygon(points=points, fill="white"))

        dwg.save()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            svg_filename = os.path.splitext(filename)[0] + ".svg"
            svg_path = os.path.join(output_folder, svg_filename)
            process_image(image_path, svg_path)
            print(f"Processed {filename} into {svg_filename}")


# # Example usage:
input_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Segmented Images/img_5"
output_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images/img_5_contour"
vectorization(input_folder, output_folder)
