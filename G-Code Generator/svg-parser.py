import xml.etree.ElementTree as ET
import math
import time


# Function to calculate the Euclidean distance between two points
def distance(cx1, cy1, cx2, cy2):
    """Calculate the distance between two points."""
    return math.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)


# Function to identify pairs of circles that are close enough to be considered connected
def find_connected_circles(circles):
    """Find circles that are close enough to be considered connected."""
    connected_pairs = []
    # Compare each circle with every other circle to find if they are connected
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            cx1, cy1, r1 = circles[i]
            cx2, cy2, r2 = circles[j]
            # If the distance is less than or equal to the sum of their radii plus a threshold, consider them connected
            if distance(cx1, cy1, cx2, cy2) <= (
                r1 + r2 + 1
            ):  # Adjust the threshold as needed
                connected_pairs.append((i, j))
    return connected_pairs


# Function to replace connected circles with lines in the SVG
def replace_circles_with_lines(tree, root, namespace, connected_pairs, circles):
    """Replace connected circles with line elements in the SVG."""
    circles_to_remove = (
        set()
    )  # Use a set to avoid duplicate removals and preserve uniqueness

    for i, j in connected_pairs:
        # Create a new line element
        line = ET.Element(
            "{http://www.w3.org/2000/svg}line",
            {
                "x1": str(circles[i][0]),
                "y1": str(circles[i][1]),
                "x2": str(circles[j][0]),
                "y2": str(circles[j][1]),
                "stroke": "white",
                "stroke-width": "1",
            },
        )
        root.append(line)  # Add the new line to the SVG root
        # Mark the original circles for removal
        circles_to_remove.add(i)
        circles_to_remove.add(j)

    # Remove marked circles
    all_circles = root.findall(".//svg:circle", namespace)
    for index in sorted(circles_to_remove, reverse=True):
        root.remove(all_circles[index])


# Main function to parse an SVG file and modify it by replacing connected circles with lines
def parse_svg(svg_file_path):
    start_time = time.time()  # Record start time

    # Parse the SVG file
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    namespace = {"svg": "http://www.w3.org/2000/svg"}

    # Extract attributes of all circle elements in the SVG
    circles = [
        (
            float(circle.attrib["cx"]),
            float(circle.attrib["cy"]),
            float(circle.attrib["r"]),
        )
        for circle in root.findall(".//svg:circle", namespace)
    ]

    # Find connected circles based on their proximity
    connected_pairs = find_connected_circles(circles)

    # Replace the identified connected circles with lines
    replace_circles_with_lines(tree, root, namespace, connected_pairs, circles)

    # Save the modified SVG to a new file
    tree.write("G-Code Generator/Assets/Vectorized Images/test/azure_modified.svg")

    end_time = time.time()  # Record end time
    print(
        f"Process completed in {end_time - start_time:.2f} seconds."
    )  # Print the duration of the process


# Entry point of the script
def main():
    svg_file_path = "G-Code Generator/Assets/Vectorized Images/test/Azure.svg"
    parse_svg(svg_file_path)


if __name__ == "__main__":
    main()
