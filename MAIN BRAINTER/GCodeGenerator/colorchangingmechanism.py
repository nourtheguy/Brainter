import os

# Define the mapping of color names to Y-axis coordinates
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

# Function to read the contents of a G-code file
def read_gcode_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Function to generate G-code commands for pen change

def generate_pen_change_gcode(pen_y_position, lift_pen_height=1):
    return [
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        f"G0 X0 Y{pen_y_position} ; Move to pen position\n",
        "G0 Z0 ; Lower pen to pick up\n",
        f"G0 Z{lift_pen_height} ; Lift pen with color\n",
    ]

# Function to generate G-code commands for returning the pen
def generate_return_pen_gcode(pen_y_position, lift_pen_height=1):
    return [
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        f"G0 X0 Y{pen_y_position} ; Move to return pen position\n",
        "G0 Z0 ; Lower pen to return\n",
        f"G0 Z{lift_pen_height} ; Lift pen without color\n",
    ]


# Main function to combine all G-codes with pen changes
def combine_gcodes(folder_path, output_filename, lift_pen_height=1):
    combined_gcode = []
    # Exclude the output file if it already exists in the folder
    sorted_files = [f for f in sorted(os.listdir(folder_path)) if f != os.path.basename(output_filename)]
    
    for i, filename in enumerate(sorted_files):
        if filename.endswith('_gcode.txt'):
            color_name = filename.split('_')[0].capitalize()
            if color_name in color_to_y_position:
                pen_y_position = color_to_y_position[color_name]
                # Generate G-code to pick up the pen
                combined_gcode.extend(generate_pen_change_gcode(pen_y_position, lift_pen_height))
                # Read and append the drawing G-code
                combined_gcode.extend(read_gcode_file(os.path.join(folder_path, filename)))
                # If it's not the last file, add G-code to return the pen
                if i < len(sorted_files) - 1:
                    combined_gcode.extend(generate_return_pen_gcode(pen_y_position, lift_pen_height))
            else:
                print(f"Color '{color_name}' not recognized. Skipping file '{filename}'.")
    return combined_gcode


# Function to write the combined G-code to a file
def write_combined_gcode(combined_gcode, output_filename):
    with open(output_filename, 'w') as file:
        file.writelines(combined_gcode)

# Example usage
folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"  # Replace with the actual path to your 'brainter' folder
output_filename = 'MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter/combined_gcode.txt'  # Replace with your desired output path
combined_gcode = combine_gcodes(folder_path, output_filename)
write_combined_gcode(combined_gcode, output_filename)

