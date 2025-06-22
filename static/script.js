document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const files = document.getElementById('pdfFiles').files;
    if (files.length === 0) {
        alert("Please select PDF files to merge");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('pdfFiles', files[i]);
    }

    const response = await fetch('/merge', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        alert("Failed to merge files");
        return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "merged.pdf";
    a.click();
});

document.getElementById('ocrForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const ocrInput = document.getElementById('ocrFiles');
  const ocrFormData = new FormData();

  [...ocrInput.files].forEach(file => ocrFormData.append('files', file));

  const res = await fetch('/extract-text', {
    method: 'POST',
    body: ocrFormData
  });

  if (res.ok) {
    const data = await res.json();
    document.getElementById('ocrResult').innerText = data.extracted_text;
  } else {
    alert("Failed to extract text");
  }
});

