document.getElementById('edit-form').onsubmit = async function(e) {
    e.preventDefault();
    document.getElementById('progress-bar').style.display = 'block';
    document.getElementById('progress').style.width = '0%';
    document.getElementById('progress').innerText = '0%';
    document.getElementById('log').innerText = '';
    const formData = new FormData(this);
    // Gửi dữ liệu lên backend
    try {
        const resp = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        document.getElementById('progress').style.width = '100%';
        document.getElementById('progress').innerText = '100%';
        document.getElementById('log').innerText = 'Đã lưu file:\n' +
            (data.txt_file ? ('- TXT: ' + data.txt_file + '\n') : '') +
            (data.img_file ? ('- Ảnh: ' + data.img_file + '\n') : '');
    } catch (err) {
        document.getElementById('log').innerText = 'Lỗi gửi dữ liệu: ' + err;
    }
};
