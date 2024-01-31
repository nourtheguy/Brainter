from PIL import Image
import svgwrite
import numpy as np


def image_to_svg(image_path, svg_path):
    # Load the image
    img = Image.open(image_path).convert("L")  # Convert to grayscale

    # Initialize SVG drawing
    dwg = svgwrite.Drawing(svg_path, profile="tiny")

    # Process the image (example: create circles for each pixel)
    pixels = np.array(img)
    for y in range(img.height):
        for x in range(img.width):
            # Set the intensity of the pixel as the radius of the circle
            radius = (255 - pixels[y, x]) / 255 * 2  # Example scale factor
            dwg.add(dwg.circle(center=(x, y), r=radius, fill="black"))

    # Save the SVG file
    dwg.save()


# Example usage
image_to_svg(
    "G-Code Generator/Assets/Segmented Images/test/Blue.png",
    "G-Code Generator/Assets/Vectorized Images/test/Blue.svg",
)
