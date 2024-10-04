import pyaudio
import json
import speech_recognition as sr
import vosk



class SpeechToText():
    
    def __init__(self, client):
        self.client = client
        
        # Initialisation Vosk
        self.vosk_model = "vosk-model-small-fr-0.22"  
        self.model = vosk.Model(self.vosk_model)

        self.p = pyaudio.PyAudio()

        # Flux audio Vosk
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000)
        self.stream.start_stream()
    

    # Détection du mot-clé
    def detect_keyword_with_vosk(self, stream, model):
        print("En attente du mot-clé 'Alexia'...")
        rec = vosk.KaldiRecognizer(model, 16000)

        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data): 
                result = json.loads(rec.Result())
                if 'text' in result and "alexia" in result['text'].lower():
                    print("Mot-clé 'Alexia' détecté !")
                    return 
            else:
                print(rec.PartialResult())  

    # Enregistrement et transcription
    def record_and_transcribe(self, client):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Parlez maintenant...")
            audio = recognizer.listen(source) 

            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

        # Speech to text
        audio_file = open("temp_audio.wav", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        print("Transcription : ", transcription.text)
        return transcription.text