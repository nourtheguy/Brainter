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

def read_gcode_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def generate_pen_pickup_gcode(pen_y_position, lift_pen_height=1):
    return [
        "G0 X1 Y0 ; Start position\n",
        f"G0 Y{pen_y_position} ; Align with pen's Y-axis at X=1\n",
        "G0 X0 ; Move to pen\n",
        "G0 Z0 ; Lower pen to pick up\n",
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        "G0 X1 ; Move back to start drawing position\n",
    ]

def generate_pen_return_gcode(pen_y_position, lift_pen_height=1):
    return [
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        f"G0 Y{pen_y_position} ; Align with pen's Y-axis at X=1\n",
        "G0 X0 ; Move to place pen back\n",
        "G0 Z0 ; Lower pen to place back\n",
        f"G0 Z{lift_pen_height} ; Lift pen\n",
        "G0 X1 ; Return to intermediate position\n",
    ]

def combine_gcodes(folder_path, output_filename, lift_pen_height=1):
    combined_gcode = ["G0 X1 Y0 ; Initial machine start position\n"]
    sorted_files = [f for f in sorted(os.listdir(folder_path)) if f != os.path.basename(output_filename)]
    
    for i, filename in enumerate(sorted_files):
        if filename.endswith('_gcode.txt'):
            color_name = filename.split('_')[0].capitalize()
            if color_name in color_to_y_position:
                pen_y_position = color_to_y_position[color_name]
                if i == 0:  # For the first pen, directly pick it up
                    combined_gcode.extend(generate_pen_pickup_gcode(pen_y_position, lift_pen_height))
                else:  # Return the previous pen and pick the next one
                    combined_gcode.extend(generate_pen_return_gcode(previous_pen_y_position, lift_pen_height))
                    combined_gcode.extend(generate_pen_pickup_gcode(pen_y_position, lift_pen_height))
                
                combined_gcode.extend(read_gcode_file(os.path.join(folder_path, filename)))
                previous_pen_y_position = pen_y_position  # Save the Y position for the next iteration
                
                if i == len(sorted_files) - 1:  # After the last drawing, return the pen
                    combined_gcode.extend(generate_pen_return_gcode(pen_y_position, lift_pen_height))
            else:
                print(f"Color '{color_name}' not recognized. Skipping file '{filename}'.")
    return combined_gcode

def write_combined_gcode(combined_gcode, output_filename):
    with open(output_filename, 'w') as file:
        file.writelines(combined_gcode)

# Example usage
folder_path = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"  # Update this path as needed
output_filename = 'MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter/combined_gcode.txt'  # Update this path as needed
combined_gcode = combine_gcodes(folder_path, output_filename)
write_combined_gcode(combined_gcode, output_filename)
