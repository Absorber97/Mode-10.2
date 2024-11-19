import click
import threading
import whisper
from queue import Queue
from .config import Config
from .audio.recorder import AudioRecorder
from .audio.transcriber import Transcriber
from .audio.responder import Responder
import os
from pathlib import Path
from openai import OpenAI
from io import BytesIO

@click.command()
@click.option("--model", default="base", help="Model to use", 
              type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Whether to use English model", 
              is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for mic detection", 
              type=int)
@click.option("--pause", default=0.8, help="Pause time before entry ends", 
              type=float)
@click.option("--dynamic_energy", default=False, help="Enable dynamic energy", 
              is_flag=True, type=bool)
@click.option("--wake_word", default="hey oak", help="Wake word to listen for", 
              type=str)
@click.option("--verbose", default=True, help="Enable verbose output", 
              is_flag=True, type=bool)
@click.option("--tts_voice", default="alloy", 
              type=click.Choice(["alloy", "echo", "fable", "onyx", "nova", "shimmer"]),
              help="OpenAI TTS voice to use")
@click.option("--tts_model", default="tts-1", 
              type=click.Choice(["tts-1", "tts-1-hd"]),
              help="OpenAI TTS model to use")
def main(**kwargs):
    # Load configuration
    config = Config.load_from_env(**kwargs)
    
    if not config.api_key:
        raise ValueError("OpenAI API key not found. Please set it in your .env file.")
    
    # Set OpenAI API key globally
    os.environ["OPENAI_API_KEY"] = config.api_key
    
    print(f"Wake word is set to: '{config.wake_word}'")
    print("Initializing components...")
    
    # Initialize queues
    audio_queue = Queue()
    result_queue = Queue()
    
    # Initialize components
    model_name = f"{config.model}.en" if config.english and config.model != "large" else config.model
    print(f"Loading Whisper model: {model_name}")
    audio_model = whisper.load_model(model_name)
    
    recorder = AudioRecorder(
        energy=config.energy,
        pause=config.pause,
        dynamic_energy=config.dynamic_energy
    )
    
    transcriber = Transcriber(
        model=audio_model,
        english=config.english,
        wake_word=config.wake_word,
        verbose=config.verbose
    )
    
    audio_handler = AudioHandler(
        temp_dir=Path("temp"),
        voice=config.tts_voice,
        model=config.tts_model
    )
    
    responder = Responder(
        api_key=config.api_key,
        verbose=config.verbose
    )

    print("Starting threads...")
    # Start threads
    threading.Thread(
        target=recorder.record,
        args=(audio_queue,),
        daemon=True
    ).start()

    threading.Thread(
        target=transcriber.transcribe,
        args=(audio_queue, result_queue),
        daemon=True
    ).start()

    threading.Thread(
        target=responder.process_responses,
        args=(result_queue,),
        daemon=True
    ).start()

    print(f"\nReady! Say '{config.wake_word}' followed by your question...")
    
    # Main loop
    try:
        while True:
            result = result_queue.get()
            if config.verbose:
                print(f"\nProcessed: {result}")
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main() 