# ScamShield - Multimodal Scam Detector

## Description
ScamShield detects scams from text and images using the Groq API and Tesseract OCR, with a Gradio interface (as seen in the provided screenshots).

## Installation
1. Clone this repo: `git clone <https://github.com/drira123/ScamShield.git>`
2. Install dependencies: `pip install groq gradio pytesseract pillow`
3. Set Tesseract path: Update `pytesseract.pytesseract.tesseract_cmd` to `C:\Program Files\Tesseract-OCR\tesseract.exe`.
4. Add your Groq API key in `detect_scam.py`.

## Usage
Run `python detect_scam.py` to launch the interface. Test with text or images, as shown in the demo.

## License
MIT# ScamShield
A multimodal scam detector
