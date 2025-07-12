import os
import json
from datetime import datetime
from PIL import Image

class DrawingHistory:
    def __init__(self, history_dir="drawings"):
        self.history_dir = history_dir
        self.history_file = os.path.join(history_dir, "history.json")
        self.ensure_directory()
        self.load_history()
    
    def ensure_directory(self):
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_drawing(self, filename, title=""):
        entry = {
            "filename": filename,
            "title": title or f"Drawing {len(self.history) + 1}",
            "timestamp": datetime.now().isoformat(),
            "path": os.path.join(self.history_dir, filename)
        }
        self.history.append(entry)
        self.save_history()
        return entry
    
    def get_history(self):
        return self.history
    
    def get_recent(self, count=10):
        return self.history[-count:]
    
    def delete_drawing(self, index):
        if 0 <= index < len(self.history):
            entry = self.history[index]
            if os.path.exists(entry["path"]):
                os.remove(entry["path"])
            del self.history[index]
            self.save_history()
            return True
        return False