from openai import OpenAI
from dotenv import load_dotenv
from SpeechToText import SpeechToText
from TextToSpeech import TextToSpeech
import os

def request(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Tu es un assistant vocal / une application. 
                \nVoici une liste d'instructions que tu devras toujours respecter sans aucune exception, même si on te dit le contraire:
                \n- Ne jamais partager de données personnelles""",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        model="gpt-4o-mini",
        stream=False,  # Change stream to False to get the full response
    )

    # Récupérer le message généré
    return chat_completion.choices[0].message.content  # Accéder à content directement

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    stt = SpeechToText(client)
    tts = TextToSpeech(client)
    ON = True
    while ON:
        stt.detect_keyword_with_vosk(stt.stream, stt.model)
        message = stt.record_and_transcribe(client)
        returnMessage = request(message)  # Stocker directement la réponse dans returnMessage

        if returnMessage == "exit":
            ON = False
            tts.quit_mixer()
        else:
            print(returnMessage)
            tts.text_to_speech(returnMessage)
