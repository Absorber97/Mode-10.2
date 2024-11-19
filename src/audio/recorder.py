from dataclasses import dataclass
import speech_recognition as sr
import torch
import numpy as np
from queue import Queue
import logging

@dataclass
class AudioRecorder:
    energy: int
    pause: float
    dynamic_energy: bool
    sample_rate: int = 16000

    def __post_init__(self):
        print("Initializing audio recorder...")
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.energy
        self.recognizer.pause_threshold = self.pause
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy
        print(f"Audio settings: energy={self.energy}, pause={self.pause}, dynamic={self.dynamic_energy}")

    def record(self, audio_queue: Queue):
        try:
            print("Opening microphone stream...")
            with sr.Microphone(sample_rate=self.sample_rate) as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"Energy threshold set to {self.recognizer.energy_threshold}")
                print("Listening...")
                
                while True:
                    try:
                        print("Waiting for audio input...")
                        audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
                        print("Audio captured, processing...")
                        audio_data = self._process_audio(audio)
                        audio_queue.put_nowait(audio_data)
                        print("Audio processed and queued")
                    except Exception as e:
                        print(f"Error in audio capture: {e}")
                        continue

        except Exception as e:
            print(f"Critical error in recording: {e}")
            raise

    def _process_audio(self, audio):
        try:
            return torch.from_numpy(
                np.frombuffer(audio.get_raw_data(), np.int16)
                .flatten()
                .astype(np.float32) / 32768.0
            )
        except Exception as e:
            print(f"Error processing audio: {e}")
            raise 