from dataclasses import dataclass
import speech_recognition as sr
import torch
import numpy as np
from queue import Queue

@dataclass
class AudioRecorder:
    energy: int
    pause: float
    dynamic_energy: bool
    sample_rate: int = 16000

    def __post_init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.energy
        self.recognizer.pause_threshold = self.pause
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy

    def record(self, audio_queue: Queue):
        with sr.Microphone(sample_rate=self.sample_rate) as source:
            print("Listening...")
            while True:
                audio = self.recognizer.listen(source)
                audio_data = self._process_audio(audio)
                audio_queue.put_nowait(audio_data)

    def _process_audio(self, audio):
        return torch.from_numpy(
            np.frombuffer(audio.get_raw_data(), np.int16)
            .flatten()
            .astype(np.float32) / 32768.0
        ) 