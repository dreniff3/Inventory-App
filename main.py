import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import re


def preprocess_image(img_path):
    '''
        Method for preprocessing image to improve OCR results.
    '''
    img = Image.open(img_path)

    # Convert image to grayscale
    img = img.convert('L')

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    # Apply sharpening filter
    img = img.filter(ImageFilter.SHARPEN)

    # Resize to make text clearer
    basewidth = 1000
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    # Save preprocessed image
    img.save('preprocessed_image.jpeg')
    return 'preprocessed_image.jpeg'


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


# Extract titles
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

    return titles


preprocessed_image = preprocess_image('dvdshelf.jpeg')
denoised_image = denoise_image(preprocessed_image)
extracted_text = extract_text(denoised_image)
extract_titles(extracted_text)
