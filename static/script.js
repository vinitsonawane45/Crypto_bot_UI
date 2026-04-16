document.addEventListener("DOMContentLoaded", () => {
    // 1. Initial Balance Check
    fetchBalance();

    // 2. Setup Toggle Switch
    const switchEl = document.getElementById("mode-switch");
    switchEl.addEventListener('change', function() {
        const mode = this.checked ? 'real' : 'demo';
        toggleMode(mode);
    });
});

function toggleMode(mode) {
    appendMessage(`System: Switching to <b>${mode.toUpperCase()}</b>...`, 'user');
    
    fetch('/api/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: mode })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            updateUI(data.mode);
            appendMessage(`✔ Mode Active: ${data.mode}`, 'success');
            fetchBalance();
        } else {
            document.getElementById("mode-switch").checked = false; // Revert toggle
            appendMessage(`✖ Connection Failed: ${data.msg}`, 'error');
        }
    });
}

function trade(side) {
    appendMessage(`> EXECUTE ${side}_ORDER`, 'user');

    fetch('/api/trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ side: side })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            const badge = data.mode === 'REAL' ? 'TESTNET' : 'SIMULATION';
            appendMessage(`
                <div style="font-size:12px; opacity:0.7; margin-bottom:4px;">[${badge}] ORDER FILLED</div>
                <b>${side}</b> @ ${data.price}<br>
                ID: ${data.id}
            `, 'success');
            fetchBalance();
        } else {
            appendMessage(`
                <div style="font-weight:bold; margin-bottom:4px;">✖ ORDER REJECTED</div>
                ${data.msg}
            `, 'error');
        }
    })
    .catch(() => appendMessage("Network Error: Backend not reachable", 'error'));
}

function fetchBalance() {
    fetch('/api/balance')
        .then(res => res.json())
        .then(data => {
            document.getElementById("balance-display").innerText = "$" + data.balance;
            updateUI(data.mode);
        });
}

function updateUI(mode) {
    const dot = document.getElementById("status-dot");
    const text = document.getElementById("connection-text");
    const switchEl = document.getElementById("mode-switch");

    if (mode === 'REAL') {
        dot.className = "status-dot online";
        text.innerText = "Connected: Testnet";
        text.style.color = "#00ff9d";
        switchEl.checked = true;
    } else {
        dot.className = "status-dot demo";
        text.innerText = "Simulation Mode";
        text.style.color = "#f59e0b";
        switchEl.checked = false;
    }
}

function appendMessage(html, type) {
    const chatFeed = document.getElementById("chat-feed");
    const div = document.createElement("div");
    
    // Map types to CSS classes
    if (type === 'user') div.className = "message msg-user";
    else if (type === 'error') div.className = "message msg-error";
    else if (type === 'success') div.className = "message msg-success";
    else div.className = "message msg-bot";

    div.innerHTML = html;
    chatFeed.appendChild(div);
    chatFeed.scrollTop = chatFeed.scrollHeight;
}