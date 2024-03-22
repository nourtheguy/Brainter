from PIL import Image


def resize_image(input_path, output_path, scale=0.6):
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the new size
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)

        # Resize the image using the LANCZOS filter for high-quality downsampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image to the output path
        resized_img.save(output_path)


# # Example usage
# input_image_path = "MAIN BRAINTER/GCodeGenerator/Assets/Images/brainter.png"
# output_image_path = "MAIN BRAINTER/GCodeGenerator/Assets/Images/brainter.png"

# resize_image(input_image_path, output_image_path)
