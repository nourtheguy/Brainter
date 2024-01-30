import cv2
import numpy as np

def color_segmentation(image, lower_bound, upper_bound):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # # Apply morphological operations to clean up the mask (optional)
    # kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.erode(mask, kernel, iterations=1)
    # mask = cv2.dilate(mask, kernel, iterations=1)

    return mask

# Example usage:
image = cv2.imread('C:/Users/ritaa/Desktop/FYP/Brainter/G-Code Generator/Assets/img_1_quantized.png')
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Call the method to get the mask for red color
red_mask = color_segmentation(image, lower_red, upper_red)

# You can use this mask for further processing or visualization
cv2.imshow('Red Mask', red_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
