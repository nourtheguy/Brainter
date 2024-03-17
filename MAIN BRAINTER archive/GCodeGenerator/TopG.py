from GCodeGenerator.color_quantization_kmeans import *
from GCodeGenerator.color_quantization_PCA import *
from GCodeGenerator.similarityscore import *
from GCodeGenerator.emptyfolder import *
from GCodeGenerator.color_segmentation import *
from GCodeGenerator.vectorization_findcontours import *
from GCodeGenerator.gcode_generation import *
from GCodeGenerator.gcode_optimization import *
from GCodeGenerator.colorchangingmechanism import *

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
gcode_text = "MAIN BRAINTER/GCodeGenerator/Assets/GCode/brainter/combined.txt"


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

    # empty folders
    empty_folder(segmentation_output_folder)
    empty_folder(vectorization_output_folder)
    empty_folder(gcode_output_folder)
    empty_folder()

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

    # GCode Generation step
    gcode_generation(vectorization_output_folder, gcode_output_folder)

    # GCode Optimization of each gcode text file
    gcode_optimization(gcode_output_folder, gcode_output_folder)

    # Color changing mechanism & combining gcode
    write_combined_gcode(combine_gcode(gcode_output_folder), gcode_text)
