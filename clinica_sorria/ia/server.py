from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo foi enviado."}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado."}), 400
        
        print('Salvando arquivo...')

        filepath = os.path.join(UPLOAD_FOLDER, 'imagem.png')
        file.save(filepath)

        # Processar a imagem
        avaliar_model(filepath)

        # Retornar a imagem processada
        print('Devolvendo imagem processada...')
        return send_file('imagem_prevista.png', mimetype='image/png')

    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return jsonify({"error": "Erro durante o processamento da imagem."}), 500

def avaliar_model(filepath):
    try:
        toPIL = transforms.ToPILImage()
        model = torch.load('UNetEfficientnetB0-best.pth').eval()
        imagem = Image.open(filepath)
        
        transformacoes = transforms.Compose([
            transforms.Resize((384, 768)),  
            transforms.ToTensor(),  
        ])

        imagem_tensor = transformacoes(imagem)

        image = imagem_tensor
        probabilities = F.sigmoid(model(image.unsqueeze(0))).squeeze(0)
        
        plt.figure(figsize=(50, 10))
        plt.subplot(1, 3, 1)
        plt.imshow(toPIL(image), cmap='gray')
        plt.title('Imagem enviada', fontsize=40)

        plt.subplot(1, 3, 2)
        plt.imshow(toPIL(probabilities), cmap='gray')
        plt.title('Localização das Cáries', fontsize=40)

        plt.subplot(1, 3, 3)
        plt.imshow(toPIL(probabilities), alpha=0.7, cmap='gray')
        plt.imshow(toPIL(image), alpha=0.5, cmap='gray')
        plt.title('Visão Geral', fontsize=40)
        
        informative_text = "Avaliação realizada por uma I.A. Recomenda-se buscar acompanhamento com o seu dentista, dando ênfase na região indicada."
        plt.figtext(0.5, 0.05, informative_text, ha="center", fontsize=30)
        
        plt.savefig('imagem_prevista.png')
        plt.close()

    except Exception as e:
        print(f"Erro durante a avaliação do modelo: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
