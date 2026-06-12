// Premium Chatbot – multiline input, syntax highlighting, fixed copy
let chatWindow = null;
let chatInput = null;
let chatBody = null;
let sendButton = null;
let expandButton = null;
let isOpen = false;
let isExpanded = false;
let isSending = false;

function initChatbot() {
    chatWindow = document.getElementById('chatbotWin');
    chatInput = document.getElementById('cwInput');
    chatBody = document.querySelector('.cw-body');
    sendButton = document.getElementById('cwSend');
    const toggleBtn = document.getElementById('chatbotToggle');
    const closeBtn = document.getElementById('cwClose');
    expandButton = document.getElementById('expandChat');

    if (toggleBtn) {
        const newToggle = toggleBtn.cloneNode(true);
        toggleBtn.parentNode.replaceChild(newToggle, toggleBtn);
        newToggle.addEventListener('click', toggleChat);
    }
    if (closeBtn) {
        const newClose = closeBtn.cloneNode(true);
        closeBtn.parentNode.replaceChild(newClose, closeBtn);
        newClose.addEventListener('click', closeChat);
    }
    if (expandButton) {
        const newExpand = expandButton.cloneNode(true);
        expandButton.parentNode.replaceChild(newExpand, expandButton);
        newExpand.addEventListener('click', toggleExpand);
        updateExpandIcon();
    }
    if (sendButton) {
        const newSend = sendButton.cloneNode(true);
        sendButton.parentNode.replaceChild(newSend, sendButton);
        newSend.addEventListener('click', sendMessage);
        sendButton = newSend;
    }
    if (chatInput) {
        const newInput = chatInput.cloneNode(true);
        chatInput.parentNode.replaceChild(newInput, chatInput);
        // Shift+Enter for newline, Enter to send
        newInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        chatInput = newInput;
        autoResizeTextarea(chatInput);
    }

    // Quick buttons
    document.querySelectorAll('.cw-quick-btn').forEach(btn => {
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
        newBtn.addEventListener('click', () => {
            if (chatInput) chatInput.value = newBtn.innerText;
            sendMessage();
        });
    });
}

function autoResizeTextarea(textarea) {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

function toggleChat() { if (isOpen) closeChat(); else openChat(); }
function openChat() {
    if (chatWindow) {
        chatWindow.classList.add('open');
        isOpen = true;
        if (chatInput) chatInput.focus();
    }
}
function closeChat() {
    if (chatWindow) {
        chatWindow.classList.remove('open');
        isOpen = false;
    }
}
function toggleExpand() {
    if (!chatWindow) return;
    if (isExpanded) {
        chatWindow.classList.remove('expanded');
        isExpanded = false;
    } else {
        chatWindow.classList.add('expanded');
        isExpanded = true;
    }
    updateExpandIcon();
}
function updateExpandIcon() {
    if (!expandButton) return;
    const icon = expandButton.querySelector('i');
    if (icon) {
        icon.setAttribute('data-lucide', isExpanded ? 'minimize-2' : 'maximize-2');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

async function sendMessage() {
    if (!chatInput) return;
    const message = chatInput.value.trim();
    if (!message) return;
    if (isSending) return;

    isSending = true;
    addMessage(message, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';
    showTypingIndicator();

    try {
        const response = await fetch('/chat/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        removeTypingIndicator();
        if (data.html) {
            addMessage(data.html, 'bot', true);
        } else if (data.reply) {
            addMessage(data.reply, 'bot');
        } else {
            addMessage('Sorry, something went wrong.', 'bot');
        }
    } catch (error) {
        console.error(error);
        removeTypingIndicator();
        addMessage('Network error. Please try again.', 'bot');
    } finally {
        isSending = false;
    }
}

function addMessage(content, sender, isHtml = false) {
    if (!chatBody) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = `cw-msg cw-${sender}`;
    if (sender === 'bot') {
        msgDiv.innerHTML = `<div class="cw-msg-av"><i data-lucide="sparkles"></i></div>
                            <div class="cw-bubble">${isHtml ? content : escapeHtml(content)}</div>`;
        attachCopyButtons(msgDiv);
        // Apply syntax highlighting to code blocks
        if (typeof hljs !== 'undefined') {
            msgDiv.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
        }
    } else {
        msgDiv.innerHTML = `<div class="cw-bubble cw-user-bubble">${escapeHtml(content)}</div>`;
    }
    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function attachCopyButtons(container) {
    const codeBlocks = container.querySelectorAll('pre');
    codeBlocks.forEach(pre => {
        if (pre.parentElement.classList.contains('code-block-wrapper')) return;
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        const btn = document.createElement('button');
        btn.className = 'copy-code-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', async () => {
            const code = pre.querySelector('code')?.innerText || pre.innerText;
            await navigator.clipboard.writeText(code);
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 1500);
        });
        wrapper.appendChild(btn);
    });
}

function showTypingIndicator() {
    if (!chatBody) return;
    removeTypingIndicator();
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'cw-msg cw-bot';
    typingDiv.innerHTML = `<div class="cw-msg-av"><i data-lucide="sparkles"></i></div>
                           <div class="cw-bubble typing"><span></span><span></span><span></span></div>`;
    chatBody.appendChild(typingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
} else {
    initChatbot();
}