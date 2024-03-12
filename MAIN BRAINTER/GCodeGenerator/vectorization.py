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
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(img, 1000, 1400)
        img_edges = Image.fromarray(edges)
        dwg = svgwrite.Drawing(svg_path, profile="tiny")
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))
        pixels = np.array(img_edges)
        for y in range(img_edges.height):
            for x in range(img_edges.width):
                if pixels[y, x]:
                    radius = 1
                    dwg.add(dwg.circle(center=(x, y), r=radius, fill="white"))
        dwg.save()

    start_time = time.time()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            svg_filename = os.path.splitext(filename)[0] + ".svg"
            svg_path = os.path.join(output_folder, svg_filename)
            image_to_svg_with_edge_detection(image_path, svg_path)
            print(f"Processed {filename} into {svg_filename}")

    duration = time.time() - start_time
    print(f"Total processing time: {duration:.2f} seconds")


# Example usage
input_folder = "GCodeGenerator/Assets/Segmented Images/img_5"
output_folder = "GCodeGenerator/Assets/Vectorized Images/img_5"
vectorization(input_folder, output_folder)
