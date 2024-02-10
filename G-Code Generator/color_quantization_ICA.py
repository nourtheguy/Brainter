import cv2
import numpy as np
import time
from sklearn.decomposition import FastICA


def color_quantization(
    input_image_path,
    output_image_path,
    preset_colors,
    num_components=18,  # This replaces num_clusters
    max_image_size=1024,
):
    def find_closest_color(pixel, colors):
        distances = np.sqrt(np.sum((colors - pixel) ** 2, axis=1))
        return colors[np.argmin(distances)]

    def ica_extract_components(image, num_components):
        pixels = image.reshape((-1, 3))
        ica = FastICA(n_components=num_components, random_state=0)
        components = ica.fit_transform(pixels)
        components = ica.mixing_  # Get the mixing matrix used during transformation
        # Normalize the component values to be within the range of RGB values
        components = (
            255
            * (components - components.min())
            / (components.max() - components.min())
        )
        return components.astype(int)

    def map_components_to_preset(components, preset_colors):
        return np.array(
            [find_closest_color(component, preset_colors) for component in components]
        )

    def replace_colors(image, components, mapped_colors):
        new_image = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                original_color = image[i, j]
                closest_component = find_closest_color(original_color, components)
                new_color = find_closest_color(closest_component, mapped_colors)
                new_image[i, j] = new_color
        return new_image

    # Read and preprocess the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Could not read the image.")
    height, width = image.shape[:2]
    if max(height, width) > max_image_size:
        scaling_factor = max_image_size / max(height, width)
        image = cv2.resize(
            image,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv2.INTER_AREA,
        )
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # ICA process
    components = ica_extract_components(image, num_components)
    mapped_colors = map_components_to_preset(components, preset_colors)
    reduced_image = replace_colors(image, components, mapped_colors)

    # Convert back to BGR and save
    reduced_image = cv2.cvtColor(reduced_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_image_path, reduced_image)


# Preset List of colors
preset_colors = np.array(
    [
        [0, 0, 0],  # Black
        [135, 135, 135],  # Grey
        [180, 20, 20],  # Red
        [50, 160, 50],  # Green
        [50, 50, 180],  # Blue
        [60, 224, 224],  # Cyan
        [125, 47, 228],  # Purple
        [218, 218, 40],  # Yellow
        [255, 137, 38],  # Orange
        [243, 243, 243],  # Light Grey
        [24, 69, 77],  # Teal
        [0, 127, 255],  # Azure
        [170, 90, 150],  # Pink
    ]
)

# Example usage
if __name__ == "__main__":
    input_image_path = "Image Sketcher/generated_images/brainter.png"
    output_image_path = "G-Code Generator/Assets/Quantized Images/brainter_ICA.png"

    try:
        start_time = time.time()
        color_quantization(input_image_path, output_image_path, preset_colors)
        end_time = time.time()
        print(
            f"Image processed and saved successfully. Time taken: {end_time - start_time:.2f} seconds."
        )
    except Exception as e:
        print("Error:", e)
