import cv2
import pytesseract

# Set the Tesseract executable path (change this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale for better OCR performance
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to clean up the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Perform OCR
    extracted_text = pytesseract.image_to_string(thresh)
    
    return extracted_text

# Input: Path to the handwritten image
image_path = "image.png"
extracted_text = process_image(image_path)

print("Extracted Text:")
print(extracted_text)
