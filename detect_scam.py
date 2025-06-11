# 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
import os
from groq import Groq
import gradio as gr
import pytesseract
from PIL import Image

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
                {"role": "system", "content": "Tu es un assistant qui classe les messages comme arnaques ou non. Réponds avec une structure claire : 'Oui' ou 'Non', suivi d'une explication structurée avec des points numérotés (ex. : 1. Raison 1, 2. Raison 2) et une estimation de confiance sur 100% (ex. : Confiance : 85%). Si le message est ambigu, mentionne-le."},
                {"role": "user", "content": f"Est-ce que ce message est une arnaque ? {message}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de l'analyse Groq : {str(e)}"

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
        return f"**Texte extrait** : {extracted_text}\n\n**Analyse** : \n{result}"
    except Exception as e:
        return f"Erreur lors de l'extraction ou de l'analyse : {str(e)}"

# Interface Gradio
with gr.Blocks() as interface:
    gr.Markdown("# Détecteur d'Arnaques")
    gr.Markdown("Entrez un message ou uploadez une image pour vérifier s'il s'agit d'une arnaque.")
    with gr.Tab("Analyse de texte"):
        text_input = gr.Textbox(lines=2, placeholder="Entrez un message à tester ici...")
        text_output = gr.Textbox(label="Résultat")
        text_button = gr.Button("Analyser le texte")
        text_button.click(fn=detect_scam, inputs=text_input, outputs=text_output)
    with gr.Tab("Analyse d'image"):
        image_input = gr.Image(type="pil", label="Uploadez une image")
        image_output = gr.Textbox(label="Résultat")
        image_button = gr.Button("Analyser l'image")
        image_button.click(fn=detect_scam_from_image, inputs=image_input, outputs=image_output)

interface.launch()