import os
import math


# Helper function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to find the closest line's start point to the current position
def find_closest_line(current_pos, remaining_lines):
    closest_line = None
    min_distance = float("inf")
    for line in remaining_lines:
        distance = calculate_distance(current_pos, line["start_pos"])
        if distance < min_distance:
            closest_line = line
            min_distance = distance
    return closest_line


# Function to generate the optimized G-code using nearest neighbor algorithm
def optimized_drawing_order(commands):
    optimized_order = []
    current_pos = (0, 0)
    remaining_lines = commands.copy()

    while remaining_lines:
        closest_line = find_closest_line(current_pos, remaining_lines)
        optimized_order.append(closest_line)
        remaining_lines.remove(closest_line)
        current_pos = closest_line["end_pos"]
    return optimized_order


# Parse G-code and extract line drawing commands with their start and end positions
def parse_gcode(gcode_lines):
    commands = []
    current_pos = (0, 0)
    for line in gcode_lines:
        if line.startswith("G0") and ("X" in line or "Y" in line):
            parts = line.split()
            for part in parts:
                if part.startswith("X"):
                    x = float(part[1:])
                    current_pos = (x, current_pos[1])
                elif part.startswith("Y"):
                    y = float(part[1:])
                    current_pos = (current_pos[0], y)
        elif line.startswith("G1") and ("X" in line or "Y" in line):
            parts = line.split()
            end_pos = current_pos
            for part in parts:
                if part.startswith("X"):
                    x = float(part[1:])
                    end_pos = (x, end_pos[1])
                elif part.startswith("Y"):
                    y = float(part[1:])
                    end_pos = (end_pos[0], y)
            commands.append({"start_pos": current_pos, "end_pos": end_pos})
            current_pos = end_pos
    return commands


# Generate optimized G-code from the optimized order
def generate_optimized_gcode(optimized_order):
    optimized_gcode = [
        "G90 ; Use absolute positioning",
        "G21 ; Set units to millimeters",
    ]
    for line in optimized_order:
        start_pos = line["start_pos"]
        end_pos = line["end_pos"]
        optimized_gcode.append(f"G0 Z1 ; Lift pen")
        optimized_gcode.append(f"G0 X{start_pos[0]} Y{start_pos[1]} ; Move to start")
        optimized_gcode.append("G0 Z0 ; Lower pen")
        optimized_gcode.append(f"G1 X{end_pos[0]} Y{end_pos[1]} ; Draw line")
    optimized_gcode.append("G0 Z1 ; Lift pen")  # Lift pen after finishing
    return optimized_gcode


# Process a single G-code file
def process_file(file_path):
    with open(file_path, "r") as file:
        gcode_lines = file.readlines()
    parsed_commands = parse_gcode(gcode_lines)
    optimized_order = optimized_drawing_order(parsed_commands)
    optimized_gcode = generate_optimized_gcode(optimized_order)
    return optimized_gcode


# Main function to process all G-code files in a directory
def gcode_optimization(source_folder_path, output_folder_path):
    # Ensure the output folder exists, if not, create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(source_folder_path):
        if filename.endswith(".txt"):  # Assuming G-code files are .txt files
            file_path = os.path.join(source_folder_path, filename)
            print(f"Processing {filename}...")
            optimized_gcode = process_file(file_path)

            # Save the optimized G-code to a new file in the output folder
            optimized_file_path = os.path.join(output_folder_path, filename)
            with open(optimized_file_path, "w") as optimized_file:
                for line in optimized_gcode:
                    optimized_file.write(f"{line}\n")
            print(f"Saved optimized G-code to {optimized_file_path}")


# if __name__ == "__main__":
#     source_folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"
#     output_folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/optimized"
#     gcode_optimization(source_folder_path, source_folder_path)
