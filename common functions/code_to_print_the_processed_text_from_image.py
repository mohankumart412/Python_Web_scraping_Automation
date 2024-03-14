import cv2
from skimage.morphology import skeletonize
import numpy as np
from easyocr import Reader

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply thresholding
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Erosion to remove small noise
    kernel = np.ones((3, 3), np.uint8)
    eroded_image = cv2.erode(binary_image, kernel, iterations=1)

    # Perform skeletonization
    skeleton = skeletonize(eroded_image / 255)

    # Invert the skeleton image
    skeleton = np.logical_not(skeleton).astype(np.uint8) * 255

    # Dilate the skeleton to fill in gaps
    dilated_skeleton = cv2.dilate(skeleton, kernel, iterations=1)

    return dilated_skeleton

def ocr_on_image(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Save the processed image (optional)
    cv2.imwrite("processed_image.png", processed_image)
    
    # Perform OCR on the processed image
    reader = Reader(['en'])
    result = reader.readtext(image_path)  # Pass the image path instead of the processed image
    
    # Extract the text from the OCR result
    captcha_text = result[0][1] if result else ""
    
    return captcha_text


# Example usage
image_path = "C:\\Users\\mohan.7482\\Desktop\\foregin trade\\Capture1.PNG"
result = ocr_on_image(image_path)
print(result)
