import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import re


# def preprocess_image(img_path):
#     '''
#         Method for preprocessing image to improve OCR results.
#     '''
#     img = Image.open(img_path)

#     # Convert image to grayscale
#     img = img.convert('L')
#     # Increase contrast
#     enhancer = ImageEnhance.Contrast(img)
#     img = enhancer.enhance(2)
#     # Apply sharpening filter
#     img = img.filter(ImageFilter.SHARPEN)
#     # Resize to make text clearer
#     basewidth = 1000
#     wpercent = basewidth / float(img.size[0])
#     hsize = int((float(img.size[1]) * float(wpercent)))
#     img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)

#     # Save preprocessed image
#     img.save('preprocessed_image.jpeg')
#     return 'preprocessed_image.jpeg'

# 1. Denoise image
def denoise_image(img_path):
    '''
        Method for denoising image to improve OCR performance.
    '''
    # Load image
    img = cv2.imread(img_path)
    # Apply Non-Local Means Denoising
    denoised_image = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    # Save and return denoised image
    cv2.imwrite('denoised_image.jpeg', denoised_image)
    return 'denoised_image.jpeg'


# 2. Deskew image
def deskew_image(img_path):
    '''
        Method for deskewing image (correcting alignment to be horizontal) for
        better recognition.
    '''
    # Load image
    img = cv2.imread(img_path)
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect edges and find skew angle
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10
        )
    angles = []
    if lines:
        for line in lines:
            for x1, y1, x2, y2 in line:
                angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                angles.append(angle)
        median_angle = np.median(angles)
        # Rotate image to deskew it
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        deskewed_image = cv2.warpAffine(
            img, M, (w, h), flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
            )
        # Save and return deskewed image
        cv2.imwrite('deskewed_image.jpeg', deskewed_image)
        return 'deskewed_image.jpeg'
    
    # Deskewing not needed
    return img_path


# 3. Thresholding (Binarization)
def binarize_image(img_path):
    '''
        Method for converting image to binary format (black and white) to
        further reduce noise/emphasize text.
    '''
    # Load image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # Apply adaptive thresholding to handle varying brightness levels
    binarized_image = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    # Save and return binarized image
    cv2.imwrite('binarized_image.jpeg', binarized_image)
    return 'binarized_image.jpeg'


# 4. Morphological Transformation (Dilation to connect text)
def apply_morphological_transform(img_path):
    '''
        Method that applies morphological transformations (dilation, erosion) to
        connect parts of text and improve consistency of characters.
    '''
    # Load image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # Apply thresholding
    _, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    # Define structuring element
    kernel = np.ones((2, 2), np.uint8)
    # Apply dilation to make characters thicker/more connected
    dilated_img = cv2.dilate(binary_img, kernel, iterations=1)
    # Save and return transformed image
    cv2.imwrite('morph_dilated_image.jpeg', dilated_img)
    return 'morph_dilated_image.jpeg'


# 5. Enhance contrast
def enhance_contrast(img_path):
    pass


# Full image processing pipeline
def process_image(img_path):
    denoised_image = denoise_image(img_path)
    deskewed_image = deskew_image(denoised_image)
    binarized_image = binarize_image(deskewed_image)
    morph_image = apply_morphological_transform(binarized_image)
    contrast_image = enhance_contrast(morph_image)
    return contrast_image


def extract_text(img_path):
    '''
        Method for extracting text from an image.
    '''
    # Initialize EasyOCR reader for English language
    reader = easyocr.Reader(['en'])

    # Use EasyOCR to read text from image
    result = reader.readtext(img_path, detail=0)

    # Extract and print text
    txt = ""
    # for (bbox, text, prob) in result:
    for text in result:
        txt += f"{text}\n"

    return txt


def extract_titles(text):
    '''
        Method for extracting titles from text using regex.
    '''
    # Use regex to find title-like patterns (capitalized words)
    # title_pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'
    title_pattern = r'([A-Z][\w\'\-:,\&\s]+(?:[A-Z][\w\'\-:,\&\s]*)+)'
    titles = re.findall(title_pattern, text)

    lines = text.split('\n')
    titles = []
    for line in lines:
        match = re.match(title_pattern, line.strip())
        if match:
            titles.append(match.group(0))

    # Remove extra whitespace
    titles = [title.strip() for title in titles]
    
    print("Detected Titles:")
    for title in titles:
        print(f"- {title}")


# extracted_text = extract_text('bookshelf.jpeg')
# print(extracted_text)

# sample_text = """
# The Great Gatsby
# Harry Potter and the Philosopher's Stone
# The Catcher in the Rye
# 1984
# To Kill a Mockingbird
# Brave New World
# The Lord of the Rings: The Fellowship of the Ring
# """
# extract_titles(sample_text)

# extracted_text = extract_text('bookshelf.jpeg')

preprocessed_image = preprocess_image('dvdshelf.jpeg')
denoised_image = denoise_image(preprocessed_image)
extracted_text = extract_text(denoised_image)
extract_titles(extracted_text)
