import os
from xml.etree import ElementTree as ET


def combine_lines(svg_content):
    root = ET.fromstring(svg_content)
    lines = root.findall(".//{http://www.w3.org/2000/svg}line")

    # Convert lines to a more convenient data structure
    line_data = [
        {
            "index": i,
            "x1": int(line.attrib["x1"]),
            "x2": int(line.attrib["x2"]),
            "y1": int(line.attrib["y1"]),
            "y2": int(line.attrib["y2"]),
        }
        for i, line in enumerate(lines)
    ]

    def can_combine(line1, line2):
        # Adjusted condition based on the new requirements
        return (
            line1["y1"] == line2["y1"]
            and line1["y2"] == line2["y2"]
            and (line1["x1"] - 1 == line2["x2"] or line1["x2"] + 1 == line2["x1"])
        )

    combined = True
    while combined:
        combined = False
        new_line_data = []
        to_remove = []
        for i, line1 in enumerate(line_data):
            if i in to_remove:  # Skip lines that are already combined
                continue
            for j, line2 in enumerate(line_data[i + 1 :], start=i + 1):
                if (
                    j in to_remove
                ):  # Ensure not to combine lines that are already combined
                    continue
                if can_combine(line1, line2):
                    # Combine lines by updating the x1 and x2 of the first line
                    line1["x1"] = min(line1["x1"], line2["x1"])
                    line1["x2"] = max(line1["x2"], line2["x2"])
                    to_remove.extend(
                        [i, j]
                    )  # Mark both lines for removal from the original list
                    new_line_data.append(line1)  # Add the newly combined line
                    combined = True
                    break  # Break to ensure we only combine with one line at a time

        line_data = [
            ld for idx, ld in enumerate(line_data) if idx not in to_remove
        ] + new_line_data

    # Create a new SVG with combined lines
    for line in lines:
        root.remove(line)  # Remove all old lines

    for line in line_data:
        ET.SubElement(
            root,
            "line",
            attrib={
                "x1": str(line["x1"]),
                "x2": str(line["x2"]),
                "y1": str(line["y1"]),
                "y2": str(line["y2"]),
                "style": "stroke:rgb(0,0,0);stroke-width:2",  # Example style, adjust as necessary
            },
        )

    return ET.tostring(root, encoding="unicode")


def process_svg_files(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.endswith(".svg"):
            continue
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            svg_content = file.read()
            modified_svg_content = combine_lines(svg_content)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_svg_content)


# Example usage
# folder_path = "path_to_your_folder"  # Update this to your SVG files' folder path
# process_svg_files(folder_path)
