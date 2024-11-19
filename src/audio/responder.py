from dataclasses import dataclass, field
from queue import Queue
from pathlib import Path
import openai
import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import logging
from typing import Optional, List
import time
from openai import OpenAI
from io import BytesIO

@dataclass
class ResponseGenerator:
    """Handles generation of responses using GPT-4"""
    system_prompt: str = """You are a helpful and concise voice assistant. 
    Provide clear, accurate, and natural-sounding responses. 
    Keep responses brief but informative, ideally under 50 words."""

    def generate(self, question: str) -> str:
        """Generate a response using GPT-4"""
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            raise

@dataclass
class AudioHandler:
    """Handles text-to-speech conversion and playback"""
    temp_dir: Path
    voice: str = "alloy"  # OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
    model: str = "tts-1"  # or tts-1-hd for higher quality
    
    def __post_init__(self):
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.client = OpenAI()
        # Initialize audio playback
        try:
            self.AudioSegment = AudioSegment
            self.play = play
        except Exception as e:
            print(f"Error initializing audio playback: {e}")
            raise

    def speak(self, text: str) -> None:
        """Convert text to speech and play it"""
        print(f"Converting to speech: {text}")
        audio_file = self.temp_dir / f"reply_{hash(text)}.mp3"
        try:
            self._generate_audio(text, audio_file)
            print("Audio generated, playing...")
            self._play_audio(audio_file)
            print("Audio playback complete")
        except Exception as e:
            print(f"Error in speak: {e}")
            raise
        finally:
            audio_file.unlink(missing_ok=True)

    def _generate_audio(self, text: str, file_path: Path) -> None:
        """Generate audio file from text using OpenAI TTS"""
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Save the audio to a file
            response.stream_to_file(str(file_path))
            if not file_path.exists():
                raise FileNotFoundError(f"Audio file was not created: {file_path}")
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            raise

    def _play_audio(self, file_path: Path) -> None:
        """Play audio file"""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            print(f"Loading audio file: {file_path}")
            audio = self.AudioSegment.from_mp3(str(file_path))
            print("Playing audio...")
            self.play(audio)
        except Exception as e:
            print(f"Error playing audio: {e}")
            raise

@dataclass
class Responder:
    """Main responder class that coordinates response generation and audio playback"""
    api_key: str
    temp_dir: Path = Path("temp")
    verbose: bool = False
    fallback_responses: List[str] = field(default_factory=lambda: [
        "I apologize, but I'm having trouble understanding. Could you rephrase that?",
        "I'm sorry, I couldn't process that request. Could you try again?",
        "I'm not sure I understood correctly. Could you explain differently?",
        "There seems to be an issue. Could you ask in a different way?"
    ])

    def __post_init__(self):
        os.environ["OPENAI_API_KEY"] = self.api_key
        openai.api_key = self.api_key
        self.generator = ResponseGenerator()
        self.audio_handler = AudioHandler(self.temp_dir)
        self.logger = logging.getLogger(__name__)
        
        if self.verbose:
            logging.basicConfig(level=logging.INFO)

    def process_responses(self, result_queue: Queue) -> None:
        """Main loop to process responses from queue"""
        while True:
            question = result_queue.get()
            if self.verbose:
                self.logger.info(f"Processing question: {question}")
            
            try:
                response = self.generator.generate(question)
                if self.verbose:
                    print(f"Generated response: {response}")
                self.audio_handler.speak(response)
            except Exception as e:
                self._handle_error(e)

    def _handle_error(self, error: Exception) -> None:
        """Handle errors during response generation or playback"""
        self.logger.error(f"Error in response processing: {error}")
        if self.verbose:
            print(f"Error: {error}")
        
        fallback = self.fallback_responses[hash(str(error)) % len(self.fallback_responses)]
        self.audio_handler.speak(fallback) 