import os

# Mapping from color names to their corresponding Y-axis positions on the pen holder
color_to_y_position = {
    "Black": 0,
    "Grey": 10,
    "Red": 20,
    "Green": 30,
    "Blue": 40,
    "Cyan": 50,
    "Purple": 60,
    "Yellow": 70,
    "Orange": 80,
    "Lightgrey": 90,
    "Teal": 100,
    "Azure": 110,
    "Pink": 120,
}


def read_gcode_file(filename):
    """
    Reads a G-code file and returns its lines as a list.

    Parameters:
    - filename: The path to the G-code file to read.

    Returns:
    - A list of strings, each representing a line in the G-code file.
    """
    with open(filename, "r") as file:
        return file.readlines()


def generate_pen_pickup_gcode(pen_y_position, lift_pen_height=1):
    """
    Generates G-code commands to pick up a pen from the specified Y-axis position.

    Parameters:
    - pen_y_position: The Y-axis position of the pen to pick up.
    - lift_pen_height: How high to lift the pen after picking it up.

    Returns:
    - A list of G-code commands as strings.
    """
    return [
        "G0 X0 Y288 ; Start position\n",
        f"G0 X{pen_y_position} ; Align with pen's Y-axis at X=1\n",
        "G0 Y290 ; Move to pen\n",
        "G0 Z0 ; Lower pen to pick up\n",
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        "G0 Y288 ; Move back to start drawing position\n",
    ]


def generate_pen_return_gcode(pen_y_position, lift_pen_height=1):
    """
    Generates G-code commands to return a pen to the specified Y-axis position.

    Parameters:
    - pen_y_position: The Y-axis position where the pen should be returned.
    - lift_pen_height: How high to lift the pen before returning it.

    Returns:
    - A list of G-code commands as strings.
    """
    return [
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        f"G0 X{pen_y_position} ; Align with pen's Y-axis at X=1\n",
        "G0 Y290 ; Move to place pen back\n",
        "G0 Z0 ; Lower pen to place back\n",
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        "G0 Y288 ; Return to intermediate position\n",
    ]


def combine_gcode(folder_path, lift_pen_height=1):
    """
    Combines G-code files from a directory, adding commands to pick up and return pens as needed.

    Parameters:
    - folder_path: The path to the directory containing the G-code files.
    - lift_pen_height: How high to lift the pen after each pick-up or return.

    Returns:
    - A list of combined G-code commands as strings.
    """
    combined_gcode = [
        "G21 ; millimeters\n",
        "G90 ; absolute coordinate\n",
        "G17 ; XY plane\n",
        "G94 ; units per minute feed rate mode\n",
        "M3 S1000 ; Turning on spindle\n",
        "G0 X0 Y0 ; Initial machine start position\n",
        "F3000\n",
    ]
    sorted_files = [
        f
        for f in sorted(os.listdir(folder_path))
        # if f != os.path.basename(output_filename)
    ]

    for i, filename in enumerate(sorted_files):
        if filename.endswith("_gcode.txt"):
            color_name = filename.split("_")[0].capitalize()
            if color_name in color_to_y_position:
                pen_y_position = color_to_y_position[color_name]
                if i == 0:  # For the first pen, directly pick it up
                    combined_gcode.extend(
                        generate_pen_pickup_gcode(pen_y_position, lift_pen_height)
                    )
                else:  # Return the previous pen and pick the next one
                    combined_gcode.extend(
                        generate_pen_return_gcode(
                            previous_pen_y_position, lift_pen_height
                        )
                    )
                    combined_gcode.extend(
                        generate_pen_pickup_gcode(pen_y_position, lift_pen_height)
                    )

                combined_gcode.extend(
                    read_gcode_file(os.path.join(folder_path, filename))
                )
                previous_pen_y_position = (
                    pen_y_position  # Save the Y position for the next iteration
                )

                if i == len(sorted_files) - 1:  # After the last drawing, return the pen
                    combined_gcode.extend(
                        generate_pen_return_gcode(pen_y_position, lift_pen_height)
                    )
            else:
                print(
                    f"Color '{color_name}' not recognized. Skipping file '{filename}'."
                )
    combined_gcode.append("G0 X0 Y0 ; Initial machine start position\n")
    combined_gcode.append("M5 ; Turning off spindle \n")
    return combined_gcode


def write_combined_gcode(combined_gcode, output_filename):
    with open(output_filename, "w") as file:
        file.writelines(combined_gcode)


# # Example usage
# folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"
# output_filename = (
#     "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter/combined_gcode.txt"
# )
# combined_gcode = combine_gcode(folder_path)
# write_combined_gcode(combined_gcode, output_filename)
