let currentAbortController = null;
let isPaused = false;
let processLogs = [];

document.getElementById('edit-form').onsubmit = async function(e) {
    e.preventDefault();
    document.getElementById('progress-bar').style.display = 'block';
    document.getElementById('control-buttons').style.display = 'block';
    document.getElementById('pause-btn').style.display = 'inline-block';
    document.getElementById('resume-btn').style.display = 'none';
    document.getElementById('progress').style.width = '0%';
    document.getElementById('progress').innerText = '0%';
    document.getElementById('log').innerText = '';
    
    isPaused = false;
    processLogs = [];
    currentAbortController = new AbortController();
    const formData = new FormData(this);
    
    // Show pause button
    document.getElementById('pause-btn').style.display = 'inline-block';
    document.getElementById('resume-btn').style.display = 'none';
    
    // Send data to backend
    try {
        const resp = await fetch('/process', {
            method: 'POST',
            body: formData,
            signal: currentAbortController.signal
        });
        
        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const text = decoder.decode(value);
            processLogs.push(text);
            document.getElementById('log').innerText += text;
            
            // Scroll to bottom
            const logElement = document.getElementById('log');
            logElement.scrollTop = logElement.scrollHeight;
        }
        
        document.getElementById('progress').style.width = '100%';
        document.getElementById('progress').innerText = '100%';
        document.getElementById('log').innerText += '\n✅ Hoàn thành!\n';
    } catch (err) {
        if (err.name === 'AbortError') {
            document.getElementById('log').innerText += '\n⚠️ Quá trình đã bị tạm dừng\n';
            document.getElementById('pause-btn').style.display = 'none';
            document.getElementById('resume-btn').style.display = 'inline-block';
        } else {
            document.getElementById('log').innerText = 'Lỗi gửi dữ liệu: ' + err;
        }
    }
};

// Pause button functionality
document.getElementById('pause-btn').onclick = function() {
    if (currentAbortController) {
        currentAbortController.abort();
        isPaused = true;
        document.getElementById('pause-btn').style.display = 'none';
        document.getElementById('resume-btn').style.display = 'inline-block';
        document.getElementById('log').innerText += '\n⏸️ Đã tạm dừng xử lý...\n';
    }
};

// Resume button functionality
document.getElementById('resume-btn').onclick = async function() {
    document.getElementById('log').innerText += '\n▶️ Đang tiếp tục xử lý...\n';
    document.getElementById('resume-btn').style.display = 'none';
    document.getElementById('pause-btn').style.display = 'inline-block';
    // In a real implementation, you would need to send a request to resume processing
    // For now, we'll just simulate the resume functionality
    document.getElementById('log').innerText += '💡 Tính năng tiếp tục sẽ được triển khai trong phiên bản tiếp theo\n';
};
