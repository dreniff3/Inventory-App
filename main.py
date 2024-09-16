import easyocr
from PIL import Image
import re


def extract_text(img_path):
    '''
        Method for extracting text from an image.
    '''
    # Initialize EasyOCR reader for English language
    reader = easyocr.Reader(['en'])

    # Use EasyOCR to read text from image
    result = reader.readtext(img_path)

    # Extract and print text
    txt = ""
    for (bbox, text, prob) in result:
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

extracted_text = extract_text('bookshelf.jpeg')
extract_titles(extracted_text)
