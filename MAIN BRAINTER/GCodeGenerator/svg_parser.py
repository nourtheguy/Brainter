import os
from xml.etree import ElementTree as ET


def combine_lines(svg_content):
    root = ET.fromstring(svg_content)
    namespace = "{http://www.w3.org/2000/svg}"
    lines = root.findall(f".//{namespace}line")
    grouped_lines = {}

    # Group lines by their y-coordinate
    for line in lines:
        y = line.attrib["y1"]  # Assuming horizontal lines have the same y1 and y2
        if y not in grouped_lines:
            grouped_lines[y] = []
        grouped_lines[y].append(line)

    for y, lines in grouped_lines.items():
        # Sort by x1 coordinate
        lines.sort(key=lambda line: int(line.attrib["x1"]))

        # Combine contiguous lines
        i = 0
        while i < len(lines) - 1:
            line = lines[i]
            next_line = lines[i + 1]
            if int(line.attrib["x2"]) + 1 >= int(
                next_line.attrib["x1"]
            ):  # Check if lines are contiguous
                # Combine lines
                line.attrib["x2"] = max(
                    int(line.attrib["x2"]), int(next_line.attrib["x2"])
                )
                root.remove(
                    next_line
                )  # Remove the next_line from the root as it's now combined
                lines.pop(i + 1)  # Remove the next_line from the list as well
            else:
                i += 1  # Move to the next line if no combination occurred

    # Return the modified SVG content
    return ET.tostring(root, encoding="unicode")


def restructure_gcode(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".svg"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                svg_content = file.read()
                modified_svg_content = combine_lines(svg_content)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modified_svg_content)


# Example usage
# folder_path = "path_to_your_folder"
# process_svg_files(folder_path)
