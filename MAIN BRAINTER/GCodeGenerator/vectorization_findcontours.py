from PIL import Image
import svgwrite
import numpy as np
import cv2
import os


def vectorization(input_folder, output_folder, line_spacing=1, line_thickness=1):
    """
    Process all images in the specified input folder, converting them to SVG format with dense lines
    within shape fills using contour detection, and save the results in the output folder.

    Parameters:
    - input_folder: Path to the folder containing the input images.
    - output_folder: Path to the folder where the SVG files will be saved.
    - line_spacing: The spacing between lines used to fill the shapes.
    - line_thickness: The thickness of the lines used to fill the shapes.
    """

    def draw_collinear_lines(dwg, points, line_spacing, line_thickness):
        if not points:
            return

        # Start with the first point as the starting point of a line
        start_point = points[0]
        for i in range(1, len(points)):
            current_point = points[i]
            next_point = points[i + 1] if i + 1 < len(points) else None

            # Check if the current point and the next point are collinear (i.e., have the same y-value)
            # and are close enough (i.e., their x-values are within 2 * line_spacing).
            # If they are not, or if there is no next point, draw the line from start_point to current_point
            # and update start_point to be the next point.
            if (
                not next_point
                or np.abs(current_point[0] - next_point[0]) > 2 * line_spacing
            ):
                end_point = current_point
                dwg.add(
                    dwg.line(
                        start=start_point,
                        end=end_point,
                        stroke="white",
                        stroke_width=line_thickness,
                    )
                )
                start_point = next_point if next_point else None

    def process_image(image_path, svg_path, line_spacing=1, line_thickness=1):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(
            img, 127, 255, cv2.THRESH_BINARY
        )  # Use normal thresholding
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )

        height, width = img.shape[:2]
        dwg = svgwrite.Drawing(svg_path, profile="tiny", size=(width, height))
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="black"))

        # Function to check if a point is inside any internal contour
        def is_inside_internal_contour(point, internal_contours):
            for ic in internal_contours:
                if cv2.pointPolygonTest(ic, point, False) > 0:
                    return True
            return False

        # Function to draw collinear lines
        def draw_collinear_lines(dwg, points, line_spacing, line_thickness):
            if not points:
                return

            start_point = points[0]
            for i in range(1, len(points)):
                current_point = points[i]
                next_point = points[i + 1] if i + 1 < len(points) else None

                if (
                    not next_point
                    or np.abs(current_point[0] - next_point[0]) > 2 * line_spacing
                ):
                    end_point = current_point
                    dwg.add(
                        dwg.line(
                            start=start_point,
                            end=end_point,
                            stroke="white",
                            stroke_width=line_thickness,
                        )
                    )
                    start_point = next_point if next_point else None

        # Organize contours into external and internal based on hierarchy
        external_contours = [
            contour for i, contour in enumerate(contours) if hierarchy[0][i][3] == -1
        ]
        internal_contours = [
            contour for i, contour in enumerate(contours) if hierarchy[0][i][3] != -1
        ]

        for contour in external_contours:
            x, y, w, h = cv2.boundingRect(contour)
            for line_y in range(y, y + h, line_spacing):
                points_inside_contour = []
                for line_x in range(x, x + w, 1):
                    if cv2.pointPolygonTest(contour, (line_x, line_y), False) >= 0:
                        if not is_inside_internal_contour(
                            (line_x, line_y), internal_contours
                        ):
                            points_inside_contour.append((line_x, line_y))

                draw_collinear_lines(
                    dwg, points_inside_contour, line_spacing, line_thickness
                )

        dwg.save()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            svg_filename = os.path.splitext(filename)[0] + ".svg"
            svg_path = os.path.join(output_folder, svg_filename)
            process_image(image_path, svg_path)
            print(f"Processed {filename} into {svg_filename}")


# # Example usage
# input_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Segmented Images"
# output_folder = "MAIN BRAINTER/GCodeGenerator/Assets/Vectorized Images"
# vectorization(input_folder, output_folder)
