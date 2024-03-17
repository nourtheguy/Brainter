from PIL import Image
import svgwrite
import numpy as np
import cv2  # Import OpenCV
import os  # Import the os module
import time  # Import time module for timing


def vectorization(input_folder, output_folder):
    """
    Process all images in the specified input folder, converting them to SVG format with edge detection,
    and save the results in the output folder.

    Parameters:
    - input_folder: Path to the folder containing the input images.
    - output_folder: Path to the folder where the SVG files will be saved.
    """

    def image_to_svg_with_edge_detection(image_path, svg_path):
        # Read the image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Detect edges
        edges = cv2.Canny(img, 1000, 1400)
        # Convert edges to PIL Image for easier handling
        img_edges = Image.fromarray(edges)
        # Get the dimensions of the input image
        img_width, img_height = img.shape[1], img.shape[0]
        # Initialize the SVG drawing with the same dimensions as the input image
        dwg = svgwrite.Drawing(svg_path, size=(img_width, img_height), profile="tiny")
        # Set the background to black
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))
        # Go through the pixels and add a circle for each white pixel in the edge detection result
        pixels = np.array(img_edges)
        for y in range(img_edges.height):
            for x in range(img_edges.width):
                if pixels[y, x]:  # If the pixel is white
                    radius = 1
                    dwg.add(dwg.circle(center=(x, y), r=radius, fill="white"))
        # Save the SVG file
        dwg.save()

    # Check if the output folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            svg_filename = os.path.splitext(filename)[0] + ".svg"
            svg_path = os.path.join(output_folder, svg_filename)
            image_to_svg_with_edge_detection(image_path, svg_path)
            print(f"Processed {filename} into {svg_filename}")


# # Example usage
# input_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Segmented Images/img_5"
# output_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images/img_5"
# vectorization(input_folder, output_folder)
