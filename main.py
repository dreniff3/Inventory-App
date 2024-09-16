import easyocr
from PIL import Image


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


extracted_text = extract_text('bookshelf.jpeg')
print(extracted_text)
