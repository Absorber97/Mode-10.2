from dataclasses import dataclass
from queue import Queue
import re
import whisper
from typing import Union, Any

@dataclass
class Transcriber:
    model: whisper.Whisper
    english: bool
    wake_word: str
    verbose: bool

    def transcribe(self, audio_queue: Queue, result_queue: Queue) -> None:
        while True:
            audio_data = audio_queue.get()
            predicted_text = self._process_audio(audio_data)
            
            if isinstance(predicted_text, str) and self._should_process(predicted_text):
                cleaned_text = self._clean_text(predicted_text)
                if self.verbose:
                    print(f"Processing: {cleaned_text}")
                result_queue.put_nowait(cleaned_text)
            elif self.verbose:
                print("Wake word not detected. Ignoring.")

    def _process_audio(self, audio_data: Any) -> str:
        result = self.model.transcribe(
            audio_data, 
            language='english' if self.english else None,
            fp16=False  # Force FP32 to avoid warning
        )
        return str(result["text"])

    def _should_process(self, text: str) -> bool:
        return text.strip().lower().startswith(self.wake_word.strip().lower())

    def _clean_text(self, text: str) -> str:
        pattern = re.compile(re.escape(self.wake_word), re.IGNORECASE)
        text = pattern.sub("", text).strip()
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        return text.translate({ord(i): None for i in punc}) 