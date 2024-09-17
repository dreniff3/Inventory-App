## Inventory App - Shelf Title Extractor

This project processes an image of a bookshelf or DVD shelf and generates a list of titles from the image using Optical Character Recognition (OCR) powered by the **EasyOCR** library.

### Installation

1. Clone this repository
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

NOTE: It's recommended to install packages in a virtual environment.

### Usage

1. Add an image of your bookshelf or DVD shelf (in `.jpg`, `.jpeg`, or `.png` format) to the project directory. Update the image path in the script to reflect your image's filename (the default is `dvdshelf.jpeg`).
2. Run the script to process the image, extract the text, and detect the titles:
   ```
   python main.py
   ```
4. The program will display the extracted titles in the console.
NOTE: The current version of the project has trouble processing non-standard text. For example, when the default `dvdshelf.jpeg` image is processed, the output to the console looks like this:

![Screenshot 2024-09-17 031315](https://github.com/user-attachments/assets/1f953eeb-103c-470f-bcbc-bad5934aafd1)

### How It Works

1. **Preprocessing:**
   - The image is first converted to grayscale and resized to enhance the visibility of the text.
   - Contrast enhancement and sharpening filters are applied to make the text stand out.
   - The preprocessed image is saved as `preprocessed_image.jpeg`.
2. **Denoising:**
   - The preprocessed image is further denoised using **OpenCV**’s Non-Local Means Denoising to reduce background noise and improve OCR results.
   - The denoised image is saved as `denoised_image.jpeg`.
3. **Text Extraction:**
   - **EasyOCR** reads the text from the denoised image and returns the extracted content as plain text.
4. **Title Extraction:**
   - A regular expression pattern is used to identify potential book or DVD titles from the OCR text output. The program looks for lines of text that follow common title conventions (e.g., capitalized words).
   - The titles are then formatted and printed in the console. 
