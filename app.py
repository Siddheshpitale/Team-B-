from flask import Flask, request, jsonify, render_template
from storage.memory_store import MemoryStore
from storage.persistence import Persistence

app = Flask(__name__)

memory = MemoryStore()
db = Persistence()

# Load stored data at startup
memory.store = db.load_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/put", methods=["POST"])
def put():
    data = request.json
    key = data.get("key")
    value = data.get("value")
    ttl = data.get("ttl")  # Optional TTL in seconds

    # Convert TTL to integer if provided
    if ttl:
        try:
            ttl = int(ttl)
        except ValueError:
            return jsonify({"error": "TTL must be a number"}), 400

    memory.put(key, value, ttl)
    
    # Get the entry with metadata for persistence
    entry = memory.store.get(key)
    if entry:
        db.put(key, entry["value"], entry["expires_at"])

    return jsonify({"message": "Data Stored Successfully"})

@app.route("/get/<key>")
def get(key):
    value = memory.get(key)
    if value is None:
        return jsonify({"error": "Key not found or expired"}), 404
    return jsonify({"value": value})

@app.route("/delete/<key>", methods=["DELETE"])
def delete(key):
    result = memory.delete(key)
    if result is None:
        return jsonify({"error": "Key not found"}), 404

    db.delete(key)
    return jsonify({"message": "Key Deleted Successfully"})

@app.route("/show")
def show():
    return jsonify(memory.get_all())

@app.route("/expire", methods=["POST"])
def expire():
    """
    Set expiration time for an existing key
    Body: {"key": "mykey", "seconds": 60}
    """
    data = request.json
    key = data.get("key")
    seconds = data.get("seconds")

    if not key or seconds is None:
        return jsonify({"error": "Key and seconds are required"}), 400

    try:
        seconds = int(seconds)
    except ValueError:
        return jsonify({"error": "Seconds must be a number"}), 400

    success = memory.expire(key, seconds)
    
    if not success:
        return jsonify({"error": "Key not found"}), 404
    
    # Update persistence
    entry = memory.store.get(key)
    if entry:
        db.put(key, entry["value"], entry["expires_at"])
    
    return jsonify({"message": f"Key will expire in {seconds} seconds"})

@app.route("/ttl/<key>")
def ttl(key):
    """
    Get remaining time to live for a key
    Returns: {"ttl": seconds} or {"ttl": -1} if no expiration, or 404 if not found
    """
    remaining = memory.ttl(key)
    
    if remaining == -2:
        return jsonify({"error": "Key not found or expired"}), 404
    
    if remaining == -1:
        return jsonify({"ttl": -1, "message": "Key has no expiration"})
    
    return jsonify({"ttl": remaining, "message": f"{remaining} seconds remaining"})

@app.route("/persist/<key>", methods=["POST"])
def persist(key):
    """
    Remove expiration from a key (make it permanent)
    """
    success = memory.persist(key)
    
    if not success:
        return jsonify({"error": "Key not found"}), 404
    
    # Update persistence
    entry = memory.store.get(key)
    if entry:
        db.put(key, entry["value"], None)
    
    return jsonify({"message": "Key is now persistent (no expiration)"})

@app.route("/stats")
def stats():
    """
    Get statistics about the key-value store
    """
    all_keys = memory.get_all()
    total_keys = len(all_keys)
    
    # Count keys with and without expiration
    with memory.lock:
        expiring_keys = sum(1 for entry in memory.store.values() if entry["expires_at"] is not None)
        persistent_keys = total_keys - expiring_keys
    
    return jsonify({
        "total_keys": total_keys,
        "persistent_keys": persistent_keys,
        "expiring_keys": expiring_keys
    })

if __name__ == "__main__":
    app.run(debug=True)