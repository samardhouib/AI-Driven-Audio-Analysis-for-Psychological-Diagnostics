import whisper
import torch

class AudioTranscriber:
    def __init__(self):
        # Check if CUDA is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load the Whisper model
        self.model = whisper.load_model("base", device=self.device)

    def transcribe_audio(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result['text'] 