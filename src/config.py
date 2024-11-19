from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Optional

@dataclass
class Config:
    model: str
    english: bool
    energy: int
    pause: float
    dynamic_energy: bool
    wake_word: str
    verbose: bool
    api_key: str
    tts_voice: str = "alloy"
    tts_model: str = "tts-1"

    @classmethod
    def load_from_env(cls, **kwargs):
        env_path = Path('.env')
        load_dotenv(env_path)
        
        api_key = os.getenv('API_KEY')
        if api_key is None:
            raise ValueError("API_KEY must be set in .env file")
            
        return cls(
            model=kwargs.get('model', 'base'),
            english=kwargs.get('english', False),
            energy=kwargs.get('energy', 300),
            pause=kwargs.get('pause', 0.8),
            dynamic_energy=kwargs.get('dynamic_energy', False),
            wake_word=kwargs.get('wake_word', 'hey oak'),
            verbose=kwargs.get('verbose', False),
            api_key=api_key,
            tts_voice=kwargs.get('tts_voice', 'alloy'),
            tts_model=kwargs.get('tts_model', 'tts-1')
        ) 