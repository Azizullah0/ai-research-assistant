import os
import whisper
from markitdown import MarkItDown
from typing import List, Dict, Any

class AgentEngine:
    def __init__(self, model: str = "llama3.2-vision"):
        self.model = model
        self.docs_dir = "my_docs"
        self.md = MarkItDown()
        # Loading 'tiny' for speed on Ubuntu CPU
        self.stt = whisper.load_model("tiny") 
        os.makedirs(self.docs_dir, exist_ok=True)

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        temp_file = "temp_recording.wav"
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)
        result = self.stt.transcribe(temp_file)
        os.remove(temp_file)
        return result["text"]

    def process_file(self, uploaded_file) -> Dict[str, Any]:
        """Saves file and returns content or image bytes."""
        file_path = os.path.join(self.docs_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if "image" in uploaded_file.type:
            return {"type": "image", "content": uploaded_file.getvalue()}
        
        try:
            conversion = self.md.convert(file_path)
            return {"type": "text", "content": conversion.text_content}
        except Exception as e:
            return {"type": "error", "content": str(e)}

    def get_tools(self) -> List[Dict[str, Any]]:
        return [{
            'type': 'function',
            'function': {
                'name': 'web_search',
                'description': 'Search a URL for live information',
                'parameters': {
                    'type': 'object',
                    'properties': {'url': {'type': 'string'}},
                    'required': ['url']
                }
            }
        }]