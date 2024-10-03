from openai import OpenAI
from dotenv import load_dotenv
from SpeechToText import SpeechToText
import os


def request(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-4o-mini",
        stream=True,
    )
    for chunk in chat_completion:
        print(chunk.choices[0].delta.content or "", end="")
        
if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    spp = SpeechToText(client)
    spp.detect_keyword_with_vosk(spp.stream, spp.model)
    message = spp.record_and_transcribe(client)
    request(message)