from setuptools import setup, find_packages

setup(
    name="voice-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "SpeechRecognition",
        "openai-whisper",
        "torch",
        "numpy",
        "gTTS",
        "openai",
        "click",
        "python-dotenv"
    ],
) 