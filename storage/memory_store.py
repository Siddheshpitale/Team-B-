import threading
import time

class MemoryStore:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()
        # Start background cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_expired_keys, daemon=True)
        self.cleanup_thread.start()

    def put(self, key, value, ttl=None):
        """
        Store a key-value pair with optional TTL
        :param key: Key to store
        :param value: Value to store
        :param ttl: Time to live in seconds (None = no expiration)
        """
        with self.lock:
            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl
            
            self.store[key] = {
                "value": value,
                "expires_at": expires_at
            }

    def get(self, key):
        """
        Get value for a key (returns None if expired or not found)
        """
        with self.lock:
            if key not in self.store:
                return None
            
            entry = self.store[key]
            
            # Check if expired
            if entry["expires_at"] is not None and time.time() > entry["expires_at"]:
                # Key expired, delete it
                del self.store[key]
                return None
            
            return entry["value"]

    def delete(self, key):
        """
        Delete a key and return its value
        """
        with self.lock:
            if key not in self.store:
                return None
            entry = self.store.pop(key)
            return entry["value"]

    def get_all(self):
        """
        Get all non-expired key-value pairs
        """
        with self.lock:
            result = {}
            current_time = time.time()
            keys_to_delete = []
            
            for key, entry in self.store.items():
                # Check if expired
                if entry["expires_at"] is not None and current_time > entry["expires_at"]:
                    keys_to_delete.append(key)
                else:
                    result[key] = entry["value"]
            
            # Clean up expired keys
            for key in keys_to_delete:
                del self.store[key]
            
            return result

    def expire(self, key, seconds):
        """
        Set expiration time for an existing key
        :param key: Key to set expiration on
        :param seconds: Seconds until expiration
        :return: True if successful, False if key not found
        """
        with self.lock:
            if key not in self.store:
                return False
            
            self.store[key]["expires_at"] = time.time() + seconds
            return True

    def ttl(self, key):
        """
        Get remaining time to live for a key
        :param key: Key to check
        :return: Remaining seconds, -1 if no expiration, -2 if key not found
        """
        with self.lock:
            if key not in self.store:
                return -2
            
            entry = self.store[key]
            
            # Check if already expired
            if entry["expires_at"] is not None and time.time() > entry["expires_at"]:
                del self.store[key]
                return -2
            
            # No expiration set
            if entry["expires_at"] is None:
                return -1
            
            # Calculate remaining time
            remaining = int(entry["expires_at"] - time.time())
            return max(0, remaining)

    def persist(self, key):
        """
        Remove expiration from a key (make it permanent)
        :param key: Key to persist
        :return: True if successful, False if key not found
        """
        with self.lock:
            if key not in self.store:
                return False
            
            self.store[key]["expires_at"] = None
            return True

    def _cleanup_expired_keys(self):
        """
        Background thread that cleans up expired keys every 60 seconds
        """
        while True:
            time.sleep(60)  # Run cleanup every minute
            with self.lock:
                current_time = time.time()
                keys_to_delete = []
                
                for key, entry in self.store.items():
                    if entry["expires_at"] is not None and current_time > entry["expires_at"]:
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self.store[key]
                
                if keys_to_delete:
                    print(f"🧹 Cleaned up {len(keys_to_delete)} expired keys")

    def get_store_with_metadata(self):
        """
        Get the raw store with all metadata (for persistence)
        """
        with self.lock:
            return dict(self.store)