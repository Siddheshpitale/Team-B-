# PyKV - Scalable In-Memory Key-Value Store with TTL Support and Persistence

**Infosys Internship Project - Batch 13**

A high-performance, persistent key-value store with automatic expiration (TTL) support, built with Python and Flask.

---

## 🚀 Features

### Core Features
- ✅ **In-Memory Storage** - Fast read/write operations using Python dictionaries
- ✅ **Persistence** - Data stored in JSON format for durability
- ✅ **Thread-Safe** - Concurrent access handling with locks
- ✅ **Web Interface** - Beautiful, responsive dashboard with animations
- ✅ **RESTful API** - Complete HTTP API for all operations

### Advanced Features (NEW!)
- ⏱️ **TTL Support** - Automatic key expiration
- 🧹 **Auto Cleanup** - Background thread removes expired keys
- 📊 **Statistics** - Real-time metrics on keys and expiration
- ♾️ **Flexible Expiration** - Set, check, or remove expiration on any key

---

## 📦 Installation

```bash
# Install dependencies
pip install flask

# Run the server
python app.py
```

Open browser: `http://localhost:5000`

---

## 🎯 TTL Operations

### 1. PUT with TTL
Store a key-value pair that expires after N seconds:

**API:**
```bash
POST /put
{
  "key": "session_token",
  "value": "abc123",
  "ttl": 3600
}
```

**Dashboard:**
- Enter key and value
- Enter TTL in seconds (optional)
- Click PUT

**Use Cases:**
- Session tokens (expire after 1 hour)
- OTP codes (expire after 5 minutes)
- Cache data (refresh every 10 minutes)

### 2. EXPIRE - Set Expiration on Existing Key
Add expiration to a key that already exists:

**API:**
```bash
POST /expire
{
  "key": "username",
  "seconds": 300
}
```

**Dashboard:**
- Enter key name
- Enter seconds until expiration
- Click SET EXPIRE

**Example:**
```
Key "username" will expire in 300 seconds (5 minutes)
```

### 3. TTL - Check Remaining Time
Check how much time is left before a key expires:

**API:**
```bash
GET /ttl/<key>
```

**Response:**
```json
{
  "ttl": 245,
  "message": "245 seconds remaining"
}
```

**Special Values:**
- `-1` = Key has no expiration (permanent)
- `-2` = Key not found or already expired

### 4. PERSIST - Remove Expiration
Make a temporary key permanent (remove its expiration):

**API:**
```bash
POST /persist/<key>
```

**Dashboard:**
- Enter key name
- Click REMOVE EXPIRE

**Result:**
```
Key is now persistent (no expiration)
```

---

## 📊 Statistics

Get real-time statistics about your key-value store:

**API:**
```bash
GET /stats
```

**Response:**
```json
{
  "total_keys": 10,
  "persistent_keys": 6,
  "expiring_keys": 4
}
```

---

## 🔧 API Reference

### Basic Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/put` | Store key-value (with optional TTL) |
| GET | `/get/<key>` | Retrieve value |
| DELETE | `/delete/<key>` | Delete key |
| GET | `/show` | Get all keys |

### TTL Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expire` | Set expiration on existing key |
| GET | `/ttl/<key>` | Check remaining time |
| POST | `/persist/<key>` | Remove expiration |
| GET | `/stats` | Get store statistics |

---

## 💾 Data Format

### JSON Storage (data.json)

**With TTL:**
```json
{
  "session:abc": {
    "value": "user_data",
    "expires_at": 1739456789.5
  },
  "username": {
    "value": "john_doe",
    "expires_at": null
  }
}
```

**Fields:**
- `value` - The actual stored value
- `expires_at` - Unix timestamp when key expires (null = no expiration)

---

## 🧹 Background Cleanup

A background thread runs every 60 seconds to clean up expired keys automatically:

```
🧹 Cleaned up 3 expired keys
```

This ensures:
- Memory is freed automatically
- Expired keys don't accumulate
- No manual cleanup needed

---

## 🎨 Web Dashboard Features

### Operations Cards
1. **PUT** - Store data with optional TTL
2. **GET** - Retrieve values
3. **DELETE** - Remove keys
4. **EXPIRE** - Set expiration time
5. **TTL** - Check time remaining
6. **PERSIST** - Make keys permanent

### Visual Feedback
- ✅ Success messages with emojis
- ❌ Error handling
- 📊 Real-time statistics
- 🎨 Animated gradient background
- ✨ Particle effects

---

## 💡 Use Cases

### 1. Session Management
```python
# Store session with 1-hour expiration
PUT session:user123 {"user_id": 123} TTL=3600

# Check remaining time
TTL session:user123  # Returns: 2847 seconds

# Extend session
EXPIRE session:user123 7200  # New 2-hour expiration
```

### 2. OTP System
```python
# Store OTP with 5-minute expiration
PUT otp:9876543210 "123456" TTL=300

# User enters OTP within 5 minutes
GET otp:9876543210  # Returns: "123456"

# After 5 minutes
GET otp:9876543210  # Returns: "Key not found or expired"
```

### 3. Cache with Auto-Refresh
```python
# Cache API response for 10 minutes
PUT cache:products "product_list_json" TTL=600

# Data refreshes automatically after 10 minutes
```

### 4. Temporary File Storage
```python
# Store temp file path for 24 hours
PUT temp:upload:xyz "/tmp/file.pdf" TTL=86400

# Make it permanent if user confirms
PERSIST temp:upload:xyz
```

---

## 🔄 Backward Compatibility

The system automatically migrates old data format to new format:

**Old Format (Before TTL):**
```json
{
  "key1": "value1",
  "key2": "value2"
}
```

**Auto-Migrates To:**
```json
{
  "key1": {"value": "value1", "expires_at": null},
  "key2": {"value": "value2", "expires_at": null}
}
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Data structures (dictionaries, thread-safe operations)
- ✅ Persistence mechanisms (JSON file storage)
- ✅ Time-based operations (TTL, expiration)
- ✅ Concurrent programming (threading, locks)
- ✅ RESTful API design
- ✅ Background job processing
- ✅ Web development (Flask, HTML, CSS, JavaScript)

---

## 📝 Project Structure

```
PyKV/
├── app.py                 # Flask application with TTL routes
├── pykv/
│   ├── config.py
│   ├── requirements.txt
│   └── __pycache__/
│                
├── storage/
│   ├── memory_store.py    # In-memory storage with TTL support
│   ├── persistence.py     # JSON persistence layer
│   ├── __init__.py
│   └── __pycache__/
├── templates/
│   ├── home.html          # Landing page
│   └── dashboard.html     # Main dashboard with TTL UI
├── static/
│   ├── style.css          # Animated styles
│   └── script.js          # TTL operations
├── database/
│   ├── kv_store.db
│   └── pykv.db        
├── data.json              # Persistent storage
└── README.md              # This file
```

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Write-Ahead Logging (WAL)
- [ ] Batch operations
- [ ] Pattern matching (KEYS *)
- [ ] Replication support
- [ ] LRU eviction policy
- [ ] Multiple data types (lists, sets, hashes)

---

## 👨‍💻 Author

**Infosys Internship - Batch 13**

Built using Python, Flask, and modern web technologies.
