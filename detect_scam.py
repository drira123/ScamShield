import os
from groq import Groq
import gradio as gr
import pytesseract
from PIL import Image
import speech_recognition as sr

# Configurer le chemin de Tesseract et TESSDATA_PREFIX
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Initialisation du client Groq
client = Groq(api_key="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")

def detect_scam(message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an assistant who classifies messages as scams or not scams. Respond with a clear structure: 'Yes' or 'No', followed by a structured explanation with numbered points (e.g., 1. Reason 1, 2. Reason 2) and a confidence estimate out of 100% (e.g., Confidence: 85%). If the message is ambiguous, please mention it.."},
                {"role": "user", "content": f"Is this message a scam? {message}"}
            ],
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during Groq analysis : {str(e)}"

def detect_scam_from_image(image):
    try:
        # Vérifier si le fichier fra.traineddata existe
        tessdata_path = os.environ.get('TESSDATA_PREFIX', '')
        fra_traineddata_path = os.path.join(tessdata_path, 'fra.traineddata')
        if not os.path.exists(fra_traineddata_path):
            return "Erreur : fra.traineddata non trouvé dans {}. Veuillez le télécharger et le placer dans le dossier tessdata.".format(tessdata_path)
        
        # Extraire le texte de l'image
        extracted_text = pytesseract.image_to_string(image, lang='fra')
        if not extracted_text.strip():
            return "Aucun texte détecté dans l'image."
        
        # Analyser le texte extrait
        result = detect_scam(extracted_text)
        return f"Texte extrait : {extracted_text}\n\n**Analyse** : \n{result}"
    except Exception as e:
        return f"Erreur lors de l'extraction ou de l'analyse : {str(e)}"

def transcribe_audio(audio_path):
    try:
        print(f"Vérification du chemin : {audio_path}")  # Débogage
        if not os.path.exists(audio_path):
            return f"Erreur : Fichier audio non trouvé à {audio_path}. Vérifiez le format (WAV requis) et rechargez-le."
        
        # Initialiser le reconnaisseur
        recognizer = sr.Recognizer()
        
        # Charger et transcrire l'audio
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="fr-FR")
            return text
    except sr.UnknownValueError:
        return "Erreur : Impossible de transcrire l'audio. Vérifiez la qualité ou le format."
    except sr.RequestError as e:
        return f"Erreur : Problème avec la reconnaissance vocale en ligne : {str(e)}"
    except Exception as e:
        return f"Erreur lors de la transcription audio : {str(e)}"

def detect_scam_from_audio(audio_path):
    try:
        print(f"Chemin audio reçu : {audio_path}")  # Débogage
        
        # Transcrire l'audio
        transcribed_text = transcribe_audio(audio_path)
        if "Erreur" in transcribed_text:
            return transcribed_text
        
        # Analyser le texte transcrit
        result = detect_scam(transcribed_text)
        return f"Texte transcrit : {transcribed_text}\n\n**Analyse** : \n{result}"
    except Exception as e:
        return f"Erreur lors de l'analyse audio : {str(e)}"


# Interface Gradio
with gr.Blocks(theme=gr.themes.Soft()) as interface:
    gr.Markdown("## 🔍 Scam Detector with AI", elem_id="main-title")
    gr.Markdown("Welcome! This system analyzes *text messages*, *images*, or *audio* to detect *potential scams*. 🚫💬🔍")

    with gr.Tab("📝 Text Analysis"):
        with gr.Row():
            with gr.Column(scale=3):
                text_input = gr.Textbox(lines=3, placeholder="Type a suspicious message to analyze...")
                text_button = gr.Button("🚨 Analyze Text", variant="primary")
            with gr.Column(scale=5):
                text_output = gr.Textbox(label="🧠 Analysis Result", lines=10)

        text_button.click(fn=detect_scam, inputs=text_input, outputs=text_output)

    with gr.Tab("🖼️ Image Analysis"):
        with gr.Row():
            with gr.Column(scale=3):
                image_input = gr.Image(type="pil", label="📷 Upload an image containing text")
                image_button = gr.Button("🧠 Analyze Image", variant="primary")
            with gr.Column(scale=5):
                image_output = gr.Textbox(label="🧠 Analysis Result", lines=10)

        image_button.click(fn=detect_scam_from_image, inputs=image_input, outputs=image_output)

    with gr.Tab("🎙️ Audio Analysis"):
        with gr.Row():
            with gr.Column(scale=3):
                audio_input = gr.Audio(label="🎧 Upload an audio file (WAV format)", type="filepath")
                audio_button = gr.Button("🧠 Analyze Audio", variant="primary")
            with gr.Column(scale=5):
                audio_output = gr.Textbox(label="🧠 Analysis Result", lines=10)

        audio_button.click(fn=detect_scam_from_audio, inputs=audio_input, outputs=audio_output)

    gr.Markdown("---")
    gr.Markdown("🛡️ This project was developed by Aicha, powered by Groq, Tesseract OCR, SpeechRecognition, and Gradio.", elem_id="footer")

interface.launch()

interface.launch()