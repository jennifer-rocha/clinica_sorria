document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const submitButton = document.getElementById('button');

    let selectedFile;

    // Detectar seleção de arquivo
    imageUpload.addEventListener('change', (event) => {
        selectedFile = event.target.files[0];
    });

    // Enviar a imagem para o servidor
    submitButton.addEventListener('click', () => {
        if (!selectedFile) {
            alert('Por favor, selecione uma imagem antes de enviar.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        })
        
        downloadAfterDelay()
        
    });
});

function downloadAfterDelay() {
    const imageUrl = 'http://127.0.0.1:5500/ia/imagem_prevista.png'; // Substitua pela URL da sua imagem

    fetch(imageUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao baixar a imagem. Código de status: ' + response.status);
        }
        return response.blob();
    })
    .then(blob => {
        // Criar um link temporário para baixar a imagem
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'imagem_prevista.png'; // Nome do arquivo a ser baixado
        downloadLink.click();
        URL.revokeObjectURL(downloadLink.href); // Liberar o objeto URL criado

        // Exibir mensagem de sucesso (opcional)
        // alert('Imagem baixada com sucesso!');
    })
}


