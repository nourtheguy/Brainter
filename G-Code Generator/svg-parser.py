import xml.etree.ElementTree as ET
import math
import time
import os


def process_all_svg_in_folder(folder_path):
    def distance(cx1, cy1, cx2, cy2):
        return math.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)

    def find_connected_circles(circles):
        connected_pairs = []
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                if distance(*circles[i][:2], *circles[j][:2]) <= (
                    circles[i][2] + circles[j][2] + 1
                ):
                    connected_pairs.append((i, j))
        return connected_pairs

    def replace_circles_with_lines(tree, root, namespace, connected_pairs, circles):
        circles_to_remove = set()
        for i, j in connected_pairs:
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
            root.append(line)
            circles_to_remove.update([i, j])

        for index in sorted(circles_to_remove, reverse=True):
            root.remove(all_circles[index])

    start_time = time.time()
    namespace = {"svg": "http://www.w3.org/2000/svg"}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".svg"):
            svg_file_path = os.path.join(folder_path, filename)
            print(f"Processing {svg_file_path}...")

            tree = ET.parse(svg_file_path)
            root = tree.getroot()

            circles = [
                (
                    float(circle.attrib["cx"]),
                    float(circle.attrib["cy"]),
                    float(circle.attrib["r"]),
                )
                for circle in root.findall(".//svg:circle", namespace)
            ]

            all_circles = root.findall(".//svg:circle", namespace)
            connected_pairs = find_connected_circles(circles)
            replace_circles_with_lines(tree, root, namespace, connected_pairs, circles)

            tree.write(svg_file_path)

    end_time = time.time()
    print(f"Completed processing all SVGs in {end_time - start_time:.2f} seconds.")


# Note: This optimization assumes no structural changes to your approach. Further optimizations might require more significant changes.
