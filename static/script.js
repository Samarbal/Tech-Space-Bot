const chatBox = document.getElementById('chatBox');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const loader = document.getElementById('loader');

// إضافة رسالة إلى الواجهة
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// إرسال السؤال إلى الخادم
async function askQuestion(question) {
    loader.style.display = 'block';
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        addMessage(data.answer, 'assistant');
        
        // إظهار المصادر (اختياري)
        if (data.sources && data.sources.length > 0) {
            const sourcesMsg = '📄 المستندات المستخدمة:\n' + data.sources.map((s, i) => `${i+1}. ${s.substring(0, 100)}...`).join('\n');
            addMessage(sourcesMsg, 'assistant');
        }
    } catch (error) {
        addMessage('⚠️ حدث خطأ: ' + error.message, 'assistant');
    } finally {
        loader.style.display = 'none';
    }
}

// معالج زر الإرسال
sendBtn.addEventListener('click', () => {
    const question = questionInput.value.trim();
    if (!question) return;
    addMessage(question, 'user');
    questionInput.value = '';
    askQuestion(question);
});

// إرسال بالضغط على Enter
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});