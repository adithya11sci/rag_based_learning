const $ = id => document.getElementById(id);
let processing = false;

// UI Elements
const els = {
    dropzone: $('dropzone'),
    fileInput: $('fileInput'),
    progress: $('progress'),
    progressBar: $('progressBar'),
    progressText: $('progressText'),
    uploadSection: $('uploadSection'),
    chatSection: $('chatSection'),
    messages: $('messages')
};

// Event Listeners
$('browseBtn').onclick = e => { e.stopPropagation(); els.fileInput.click(); };
els.dropzone.onclick = () => els.fileInput.click();
els.fileInput.onchange = e => e.target.files[0] && upload(e.target.files[0]);

els.dropzone.ondragover = e => { e.preventDefault(); els.dropzone.classList.add('drag'); };
els.dropzone.ondragleave = () => els.dropzone.classList.remove('drag');
els.dropzone.ondrop = e => {
    e.preventDefault();
    els.dropzone.classList.remove('drag');
    const file = e.dataTransfer.files[0];
    if (file?.name.endsWith('.pdf')) upload(file);
    else alert('Please upload a PDF file');
};

async function upload(file) {
    if (processing) return;
    processing = true;

    // Show progress UI
    els.progress.classList.add('show');
    updateProgress(0, 'Starting upload...');

    const form = new FormData();
    form.append('file', file);

    try {
        // Simulated upload progress
        updateProgress(30, 'Uploading document...');

        const res = await fetch('/api/upload', { method: 'POST', body: form });

        updateProgress(70, 'Processing text & index...');

        const data = await res.json();

        if (data.success) {
            updateProgress(100, 'Complete!');
            setTimeout(() => initChat(file.name, data.chunk_count), 800);
        } else {
            throw new Error(data.message);
        }
    } catch (e) {
        alert('Upload Error: ' + e.message);
        els.progress.classList.remove('show');
    }
    processing = false;
}

function updateProgress(percent, text) {
    els.progressBar.style.width = `${percent}%`;
    els.progressText.textContent = text;
}

function initChat(name, chunks) {
    els.uploadSection.hidden = true;
    els.chatSection.hidden = false;
    $('docName').textContent = `📄 ${name}`;
    $('status').textContent = 'Ready to assist';
    $('status').classList.add('active');

    els.messages.innerHTML = `
        <div class="msg bot">
            Hi! I've analyzed <b>${name}</b> (${chunks} chunks).<br>
            Ask me anything about the document!
        </div>
    `;
    $('input').focus();
}

function resetApp() {
    els.chatSection.hidden = true;
    els.uploadSection.hidden = false;
    els.progress.classList.remove('show');
    els.progressBar.style.width = '0%';
    $('status').textContent = 'Waiting for document...';
    $('status').classList.remove('active');
}

// Chat Logic
$('newBtn').onclick = async () => { await fetch('/api/clear', { method: 'POST' }); resetApp(); };

$('input').oninput = function () {
    $('sendBtn').disabled = !this.value.trim();
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
};

$('input').onkeydown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
};

$('sendBtn').onclick = sendMessage;

async function sendMessage() {
    const text = $('input').value.trim();
    if (!text || processing) return;

    processing = true;
    $('sendBtn').disabled = true;
    $('input').value = '';
    $('input').style.height = 'auto';

    // User Message
    els.messages.innerHTML += `<div class="msg user">${text}</div>`;
    scrollToBottom();

    // Typing Indicator
    const typingId = 'typing-' + Date.now();
    els.messages.innerHTML += `
        <div id="${typingId}" class="typing">
            <span></span><span></span><span></span>
        </div>
    `;
    scrollToBottom();

    try {
        const res = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: text })
        });
        const data = await res.json();

        $(typingId).remove();

        // Bot Message
        els.messages.innerHTML += `<div class="msg bot">${formatText(data.answer)}</div>`;
        scrollToBottom();

    } catch (e) {
        $(typingId).remove();
        els.messages.innerHTML += `<div class="msg bot">Error: Could not get response.</div>`;
    }

    processing = false;
    $('input').focus();
}

function formatText(text) {
    return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
}

function scrollToBottom() {
    els.messages.scrollTop = els.messages.scrollHeight;
}

// Init check
fetch('/api/status').then(r => r.json()).then(s => {
    if (s.has_document) initChat(s.pdf_name, s.chunk_count);
});
