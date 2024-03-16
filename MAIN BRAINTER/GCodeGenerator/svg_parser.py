import os
import xml.etree.ElementTree as ET
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_svg_file(svg_file_path):
    try:
        namespace = {"svg": "http://www.w3.org/2000/svg"}
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

        connected_pairs = []
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                if math.sqrt(
                    (circles[j][0] - circles[i][0]) ** 2
                    + (circles[j][1] - circles[i][1]) ** 2
                ) <= (circles[i][2] + circles[j][2] + 1):
                    connected_pairs.append((i, j))

        all_circles = root.findall(".//svg:circle", namespace)
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

        tree.write(svg_file_path)
        return f"Processed {svg_file_path}"

    except Exception as e:
        return f"Failed to process {svg_file_path}: {e}"


def process_all_svg_in_folder(folder_path):

    svg_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".svg")
    ]

    # Adjust max_workers based on your system's capabilities and the task's requirements
    with ProcessPoolExecutor(max_workers=22) as executor:
        future_to_file = {
            executor.submit(process_svg_file, file): file for file in svg_files
        }
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"{file} generated an exception: {exc}")


if __name__ == "__main__":
    vectorization_output_folder = (
        "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images/img_5"
    )
    process_all_svg_in_folder(vectorization_output_folder)
