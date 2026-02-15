function showMessage(msg) {
    document.getElementById("output").innerText = msg;
}

function putData() {
    const key = document.getElementById("putKey").value;
    const value = document.getElementById("putValue").value;
    const ttl = document.getElementById("putTTL").value;

    if (!key || !value) {
        showMessage("❌ Key and Value are required");
        return;
    }

    const body = { key, value };
    if (ttl) {
        body.ttl = parseInt(ttl);
    }

    fetch("/put", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(() => {
        if (ttl) {
            showMessage(`✅ Data Stored with ${ttl}s TTL`);
        } else {
            showMessage("✅ Data Stored Successfully");
        }
        // Clear inputs
        document.getElementById("putKey").value = "";
        document.getElementById("putValue").value = "";
        document.getElementById("putTTL").value = "";
    })
    .catch(() => {
        showMessage("❌ Error storing data");
    });
}

function getData() {
    const key = document.getElementById("getKey").value;

    if (!key) {
        showMessage("❌ Key is required");
        return;
    }

    fetch("/get/" + key)
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        showMessage("📌 Value: " + data.value);
    })
    .catch(() => {
        showMessage("❌ Key Not Found or Expired");
    });
}

function deleteData() {
    const key = document.getElementById("deleteKey").value;

    if (!key) {
        showMessage("❌ Key is required");
        return;
    }

    fetch("/delete/" + key, { method: "DELETE" })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(() => {
        showMessage("🗑️ Key Deleted Successfully");
        document.getElementById("deleteKey").value = "";
    })
    .catch(() => {
        showMessage("❌ Key Not Found");
    });
}

function showAll() {
    fetch("/show")
    .then(res => res.json())
    .then(data => {
        if (Object.keys(data).length === 0) {
            showMessage("⚠️ No Data Available");
        } else {
            document.getElementById("output").innerText =
                JSON.stringify(data, null, 2);
        }
    });
}

function expireKey() {
    const key = document.getElementById("expireKey").value;
    const seconds = document.getElementById("expireSeconds").value;

    if (!key || !seconds) {
        showMessage("❌ Key and Seconds are required");
        return;
    }

    fetch("/expire", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, seconds: parseInt(seconds) })
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        showMessage(`⏱️ ${data.message}`);
        document.getElementById("expireKey").value = "";
        document.getElementById("expireSeconds").value = "";
    })
    .catch(() => {
        showMessage("❌ Key Not Found");
    });
}

function checkTTL() {
    const key = document.getElementById("ttlKey").value;

    if (!key) {
        showMessage("❌ Key is required");
        return;
    }

    fetch("/ttl/" + key)
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        if (data.ttl === -1) {
            showMessage("♾️ Key has no expiration (permanent)");
        } else {
            showMessage(`⏰ TTL: ${data.ttl} seconds remaining`);
        }
    })
    .catch(() => {
        showMessage("❌ Key Not Found or Expired");
    });
}

function persistKey() {
    const key = document.getElementById("persistKey").value;

    if (!key) {
        showMessage("❌ Key is required");
        return;
    }

    fetch("/persist/" + key, { method: "POST" })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(data => {
        showMessage(`♾️ ${data.message}`);
        document.getElementById("persistKey").value = "";
    })
    .catch(() => {
        showMessage("❌ Key Not Found");
    });
}

function showStats() {
    fetch("/stats")
    .then(res => res.json())
    .then(data => {
        const statsMsg = `
📊 STATISTICS:
━━━━━━━━━━━━━━━━
Total Keys: ${data.total_keys}
Persistent Keys: ${data.persistent_keys}
Expiring Keys: ${data.expiring_keys}
━━━━━━━━━━━━━━━━
        `;
        showMessage(statsMsg);
    })
    .catch(() => {
        showMessage("❌ Error fetching statistics");
    });
}