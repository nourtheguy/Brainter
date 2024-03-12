from GCodeGenerator.color_quantization_kmeans import *
from GCodeGenerator.color_quantization_PCA import *
from GCodeGenerator.similarityscore import *
from GCodeGenerator.emptyfolder import *
from GCodeGenerator.color_segmentation import *
from GCodeGenerator.vectorization import *
from GCodeGenerator.svg_parser import *
from GCodeGenerator.gcode_generation import *

input_image_path = "MAIN BRAINTER/GCodeGenerator/Assets/Images/brainter.png"
output_image_path_kmeans = (
    "MAIN BRAINTER/GCodeGenerator/Assets/Quantized Images/brainter_kmeans.png"
)
output_image_path_PCA = (
    "MAIN BRAINTER/GCodeGenerator/Assets/Quantized Images/brainter_PCA.png"
)
segmentation_output_folder = (
    "MAIN BRAINTER/GCodeGenerator/Assets/Segmented Images/brainter"
)
vectorization_output_folder = (
    "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images/brainter"
)
gcode_output_folder = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter"


def TopG():

    # Quantize the received image using kmeans and PCA
    color_quantization_kmeans(input_image_path, output_image_path_kmeans, preset_colors)
    print("kmeans")
    color_quantization_PCA(input_image_path, output_image_path_PCA, preset_colors)
    print("PCA")
    print("Image Quantized")

    # Compare kmeans and PCA
    # read generated images with opencv
    original = cv2.imread(input_image_path, 0)
    Kmeans_image = cv2.imread(output_image_path_kmeans, 0)
    PCA_image = cv2.imread(output_image_path_PCA, 0)
    ssim_PCA = structural_sim(original, PCA_image)
    ssim_kmeans = structural_sim(original, Kmeans_image)

    # empty segmentation output folder
    empty_folder(segmentation_output_folder)

    # segmentation based on better method
    if ssim_PCA > ssim_kmeans:
        print("PCA is more similar to the original image based on SSIM.")
        color_segmentation(
            output_image_path_PCA,
            segmentation_output_folder,
            preset_colors,
            color_names,
        )
    else:
        print("KMeans is more similar to the original image based on SSIM.")
        color_segmentation(
            output_image_path_kmeans,
            segmentation_output_folder,
            preset_colors,
            color_names,
        )

    # vectorization step
    vectorization(segmentation_output_folder, vectorization_output_folder)
    print("Vectorization")

    # SVG manipulation step
    process_all_svg_in_folder(vectorization_output_folder)

    # GCode Generation step
    gcode_generation(vectorization_output_folder, gcode_output_folder)
