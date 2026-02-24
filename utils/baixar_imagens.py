import os
import requests
from PIL import Image
from io import BytesIO

def baixar_imagens(urls, nome_pagina, demanda_id):
    """
    Baixa imagens de uma lista de URLs, remove transparência (alpha),
    redimensiona para 502x376 e salva no diretório
    'app/routes/generate_pdf/{nome_pagina}_{demanda_id}'.

    Args:
        urls (list): Lista de URLs (strings ou listas com uma string).
        nome_pagina (str): Nome da página (ex: "narrative").
        demanda_id (int or str): Identificador único da demanda.

    Returns:
        list: Lista de caminhos dos arquivos salvos.
    """
    base_dir = os.path.join("app", "routes", "generate_pdf")
    pasta_destino = os.path.join(base_dir, f"{nome_pagina}_{demanda_id}")
    os.makedirs(pasta_destino, exist_ok=True)

    caminhos_salvos = []

    for idx, url in enumerate(urls, start=1):
        final_url = url[0] if isinstance(url, list) else url
        try:
            response = requests.get(final_url, timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))

            # Remove transparência, preenchendo com branco
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert("RGB")

            img = img.resize((502, 376), Image.LANCZOS)

            caminho_arquivo = os.path.join(pasta_destino, f"imagem_{idx}.jpg")
            img.save(caminho_arquivo, format="JPEG", quality=85)

            caminhos_salvos.append(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao baixar ou processar imagem {final_url}: {e}")

    return caminhos_salvos
