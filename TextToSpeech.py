from openai import OpenAI
import pygame
import time
import os
import pathlib

class TextToSpeech():
    
    def __init__(self, client):
        self.client = client
    
    def text_to_speech(self, text):

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )

        audio_file = "output.mp3"

        response.stream_to_file(audio_file)
    
        if os.path.exists(audio_file):
            pygame.mixer.init()
            print(f"{audio_file} a été créé avec succès.")
            
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pathlib.Path(audio_file).unlink()
            
        else:
            print(f"Erreur : {audio_file} n'a pas été créé.")
    
    def quit_mixer(self):
        pygame.mixer.quit()