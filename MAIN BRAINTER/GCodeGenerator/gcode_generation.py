import xml.etree.ElementTree as ET
import os
import time
import glob


def gcode_generation(input_directory, output_directory):
    def parse_svg_file(svg_file_path):
        ns = {"ns0": "http://www.w3.org/2000/svg"}
        tree = ET.parse(svg_file_path)
        root = tree.getroot()
        lines = root.findall(".//ns0:line", ns)
        return lines

    def svg_to_gcode(lines):
        gcode = ["G90 ; Use absolute positioning", "G21 ; Set units to millimeters"]
        for line in lines:
            x1, y1, x2, y2 = (
                line.get("x1"),
                line.get("y1"),
                line.get("x2"),
                line.get("y2"),
            )
            gcode += [
                "G0 Z20 ; Lift pen",
                f"G0 X{x1} Y{y1} ; Move to start",
                "G0 Z0 ; Lower pen",
                f"G1 X{x2} Y{y2} ; Draw line",
            ]
        gcode.append("G0 Z20 ; Lift pen")
        return gcode

    def generate_gcode_for_svg(svg_file_path, output_directory):
        lines = parse_svg_file(svg_file_path)
        gcode = svg_to_gcode(lines)
        os.makedirs(output_directory, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(svg_file_path))[0]
        gcode_file_name = f"{base_name}_gcode.txt"
        gcode_file_path = os.path.join(output_directory, gcode_file_name)
        with open(gcode_file_path, "w") as f:
            for line in gcode:
                f.write(f"{line}\n")
        print(
            f"G-code generated for: {os.path.basename(svg_file_path)} -> {gcode_file_name}"
        )

    # start_time = time.time()
    svg_files = glob.glob(os.path.join(input_directory, "*.svg"))
    for svg_file in svg_files:
        generate_gcode_for_svg(svg_file, output_directory)
    # end_time = time.time()
    # print(f"All SVG files processed. Duration: {end_time - start_time:.2f} seconds.")


# # Usage
# input_directory = "GCodeGenerator/Assets/Vectorized Images/img_5"
# output_directory = "GCodeGenerator/Assets/GCode/img_5"

# gcode_generation(input_directory, output_directory)
