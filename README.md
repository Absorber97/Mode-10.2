# AI Voice Assistant (OpenAI TTS)

A modern voice assistant powered by OpenAI's GPT-4 and Whisper models. This assistant can understand voice commands, process them using advanced AI, and respond naturally through speech.

## 🌟 Features

- 🎙️ **Voice Activation** - Customizable wake word (default: "hey oak")
- 🤖 **GPT-4 Integration** - Advanced natural language processing
- 🗣️ **Whisper ASR** - Accurate speech-to-text conversion
- 🔊 **OpenAI TTS** - High-quality voice responses with multiple voice options
- 🎛️ **Configurable Settings** - Adjust sensitivity, language, voice, and more
- 📝 **Verbose Mode** - Detailed operation logging

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd voice-assistant
   ```

2. **Install System Dependencies**

   macOS:
   ```bash
   brew install portaudio ffmpeg
   ```

   Ubuntu/Debian:
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg
   ```

3. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API**
   Create a `.env` file in the project root:
   ```
   API_KEY=your_openai_api_key_here
   ```

5. **Run the Assistant**
   ```bash
   python run.py
   ```

## ⚙️ Command Line Options

bash
python run.py [OPTIONS]
Options:
--model [tiny|base|small|medium|large] Whisper model size (default: base)
--english Use English-specific model
--energy INTEGER Mic sensitivity (default: 300)
--pause FLOAT Pause threshold (default: 0.8)
--dynamic_energy Enable dynamic energy
--wake_word TEXT Custom wake word (default: "hey oak")
--verbose Enable detailed logging



## 📦 Project Structure

   ```
voice-assistant/
├── src/
│ ├── audio/
│ │ ├── recorder.py # Audio recording
│ │ ├── transcriber.py # Speech recognition
│ │ └── responder.py # GPT response handling
│ ├── config.py # Configuration
│ └── voice_assistant.py # Main application
├── .env # API keys
├── requirements.txt # Dependencies
└── run.py # Entry point
   ```


## 🎯 Usage Examples

1. **Basic Usage**
   ```bash
   python run.py
   ```
   Say "hey oak" followed by your question.

2. **High Accuracy Mode**
   ```bash
   python run.py --model medium --english --verbose
   ```

3. **Custom Wake Word**
   ```bash
   python run.py --wake_word "hello assistant"
   ```

4. **Noisy Environment**
   ```bash
   python run.py --energy 400 --dynamic_energy
   ```

## 🔧 Troubleshooting

### Common Issues

1. **No Microphone Input**
   - Check microphone connections
   - Verify system permissions
   - Try increasing `--energy` value

2. **High CPU Usage**
   - Use smaller model (`--model tiny`)
   - Increase pause threshold
   - Disable verbose mode

3. **API Errors**
   - Verify API key in `.env`
   - Check internet connection
   - Ensure OpenAI account has credits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 Requirements

- Python 3.8+
- FFmpeg
- Portaudio
- OpenAI API key
- Internet connection

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-4, Whisper, and Text-to-Speech
- Open source community

## 🔗 Links

- [OpenAI Platform](https://platform.openai.com)
- [Whisper Documentation](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org)