import json
import os
import threading

class Persistence:
    def __init__(self, filepath="data.json"):
        self.filepath = filepath
        self.lock = threading.Lock()
    
    def put(self, key, value, expires_at=None):
        """
        Persist a key-value pair with optional expiration
        :param key: Key to store
        :param value: Value to store
        :param expires_at: Expiration timestamp (None = no expiration)
        """
        with self.lock:
            data = self.load_all()
            data[key] = {
                "value": value,
                "expires_at": expires_at
            }
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    def load_all(self):
        """
        Load all data from JSON file
        """
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                
                # Handle backward compatibility with old format
                # Old format: {"key": "value"}
                # New format: {"key": {"value": "...", "expires_at": ...}}
                migrated_data = {}
                for key, val in data.items():
                    if isinstance(val, dict) and "value" in val:
                        # New format
                        migrated_data[key] = val
                    else:
                        # Old format - migrate to new format
                        migrated_data[key] = {
                            "value": val,
                            "expires_at": None
                        }
                
                return migrated_data
        return {}
    
    def delete(self, key):
        """
        Delete a key from persistent storage
        """
        with self.lock:
            data = self.load_all()
            if key in data:
                del data[key]
                with open(self.filepath, 'w') as f:
                    json.dump(data, f, indent=2)
    
    def save_all(self, store_data):
        """
        Save entire store to disk (used for batch updates)
        :param store_data: Dictionary with metadata structure
        """
        with self.lock:
            with open(self.filepath, 'w') as f:
                json.dump(store_data, f, indent=2)