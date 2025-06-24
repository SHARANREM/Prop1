async function generateCode() {
    const text = document.getElementById('textInput').value;
    const res = await fetch('/generate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    });
    const data = await res.json();
    document.getElementById('codeOutput').innerText = data.unique_code;
}

async function convertDocx() {
    const fileInput = document.getElementById('docxFile');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const res = await fetch('/convert-docx', { method: 'POST', body: formData });
    if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        window.open(url);
    } else {
        const data = await res.json();
        alert(data.error);
    }
}
