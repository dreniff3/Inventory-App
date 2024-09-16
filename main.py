import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import re


def preprocess_image(img_path):
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
    title_pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'
    titles = re.findall(title_pattern, text)
    
    print("Detected Titles:")
    for title in titles:
        print(f"- {title}")


# extracted_text = extract_text('bookshelf.jpeg')
# print(extracted_text)

# sample_text = """The Great Gatsby
# Harry Potter and the Philosopher's Stone
# The Catcher in the Rye"""
# extract_titles(sample_text)

# extracted_text = extract_text('bookshelf.jpeg')
preprocessed_image = preprocess_image('dvdshelf.jpeg')
extracted_text = extract_text(preprocessed_image)
extract_titles(extracted_text)
