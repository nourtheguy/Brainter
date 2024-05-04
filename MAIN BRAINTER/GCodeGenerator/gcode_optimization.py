import os
import math
from concurrent.futures import ProcessPoolExecutor, as_completed


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


# Helper function to merge consecutive lines that are directly connected or separated by 1 in Y
def merge_consecutive_lines(lines):
    merged_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i]
        while i + 1 < len(lines) and can_merge(current_line, lines[i + 1]):
            next_line = lines[i + 1]
            current_line = {
                "start_pos": current_line["start_pos"],
                "end_pos": next_line["end_pos"],
            }
            i += 1
        merged_lines.append(current_line)
        i += 1
    return merged_lines


# Check if two lines can be merged with additional X range condition and adjusted Y continuity check
def can_merge(line1, line2):
    x_range_ok = abs(line1["end_pos"][0] - line2["start_pos"][0]) <= 3
    y_continuity = abs(line2["start_pos"][1] - line1["end_pos"][1]) <= 2

    return y_continuity and x_range_ok


# Update the generate_optimized_gcode function to handle pen lifts and drops for non-continuations
def generate_optimized_gcode(optimized_order):
    optimized_gcode = [
        "G90 ; Use absolute positioning",
        "G21 ; Set units to millimeters",
        # "G0 Z40 ; Lift pen initially",
    ]
    # Merge consecutive lines before generating G-code
    merged_lines = merge_consecutive_lines(optimized_order)
    last_pos = (0, 0)
    for line in merged_lines:
        start_pos = line["start_pos"]
        end_pos = line["end_pos"]
        # Only lift and lower the pen if moving to a new start position that isn't a direct continuation
        if last_pos != start_pos:
            if (
                abs(last_pos[1] - start_pos[1]) > 2
            ):  # Check if Y continuity is broken beyond ±2 units
                optimized_gcode.append(
                    f"G0 Z40 ; Lift pen before moving to a new start"
                )
            optimized_gcode.append(
                f"G0 X{start_pos[0]} Y{start_pos[1]} ; Move to start"
            )
            optimized_gcode.append(f"G0 Z0 ; Lower pen to start drawing")
        optimized_gcode.append(f"G1 X{end_pos[0]} Y{end_pos[1]} ; Draw line")
        last_pos = end_pos
    optimized_gcode.append("G0 Z40 ; Lift pen after finishing")
    return optimized_gcode


# Process a single G-code file
def process_file(file_path):
    # Assuming this function is unchanged, except you might need to handle exceptions or issues within the file processing more gracefully
    try:
        with open(file_path, "r") as file:
            gcode_lines = file.readlines()
        parsed_commands = parse_gcode(gcode_lines)
        optimized_order = optimized_drawing_order(parsed_commands)
        optimized_gcode = generate_optimized_gcode(optimized_order)
        return optimized_gcode
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def save_optimized_gcode(file_path, optimized_gcode):
    if optimized_gcode is not None:
        with open(file_path, "w") as optimized_file:
            for line in optimized_gcode:
                optimized_file.write(f"{line}\n")
        return f"Saved optimized G-code to {file_path}"
    else:
        return f"Failed to save optimized G-code for {file_path}"


def gcode_optimization(source_folder_path, output_folder_path, max_workers=22):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    gcode_files = [
        os.path.join(source_folder_path, f)
        for f in os.listdir(source_folder_path)
        if f.endswith(".txt")
    ]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_file, file): file for file in gcode_files
        }

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                optimized_gcode = future.result()
                optimized_file_path = os.path.join(
                    output_folder_path, os.path.basename(file)
                )
                result = save_optimized_gcode(optimized_file_path, optimized_gcode)
                print(result)
            except Exception as exc:
                print(f"{file} generated an exception: {exc}")


# if __name__ == "__main__":
#     source_folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"
#     output_folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/optimized"
#     gcode_optimization(source_folder_path, source_folder_path)
